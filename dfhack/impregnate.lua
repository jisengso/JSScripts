-- Impregnates a creature(s)

--[====[
If female has spouse, use spouse's information.
If female has no spouse and is an adult, randomize genes.

impregnate           If the cursor points at a creature, impregnate it.
impregnate -query    Displays would-be-affected creatures without action.
impregnate -all      Affects all creatures in local site.
impregnate -species  Affects all individuals of the same species as the selected creature.

-all, takes precedent over -species.
May not work for species with other than 2 genders.

]====]

local args = {...}
local pregList = {}

local pregRng = dfhack.random.new()
local doingQuery = 0
local doingAll = 0
local doingSpecies = 0

if not dfhack.isWorldLoaded() then
    qerror('World not loaded.')
end

world = df.global.world

function evalArgs()
    if #args > 0 then
        for _,arg in pairs(args) do
            if arg == '-query' then
                doingQuery = 1
            end
            if arg == '-all' then
                doingAll = 1
            end
            if arg == '-species' then
                doingSpecies = 1
            end
        end
    end
end

function suitableMother(unit)
    -- Professions 103 and 104 are 'baby' and 'child'. Even applies to cats.
    if dfhack.units.isAlive(unit) and dfhack.units.isVisible(unit) and dfhack.units.isFemale(unit) and not (unit.profession == 103) and not (unit.profession == 104) then
        return true
    end
    return false
end

function makeList()
    local tmpList = {}
    if doingAll == 0 and doingSpecies == 0 then
        local newMother = dfhack.gui.getSelectedUnit()
        if newMother == nil or not dfhack.units.isFemale(newMother) then
            print("Unsuitable mother error.")
            return tmpList
        end
        table.insert(tmpList, newMother);
        return tmpList
    end
    if doingAll == 1 then
        for _, unit in pairs(world.units.all) do
            -- Evaluates adulthood by if the creature is more than 12 years old. May not be accurate for all species.
            if suitableMother(unit) then
                table.insert(tmpList, unit)
            end
        end
    elseif doingSpecies == 1 then
        local motherIndividual = dfhack.gui.getSelectedUnit()
        if motherIndividual == nil then
            return tmpList
        end
        local motherSpecies = motherIndividual.race
        for _, unit in pairs(world.units.all) do
            if suitableMother(unit) and unit.race == motherSpecies then
                table.insert(tmpList, unit)
            end            
        end
    end    
    return tmpList
end

function impregnate (unit)

    local newMother = unit;
    local spouseId = newMother.relationship_ids[1];
    local spouse = df.unit.find(spouseId);
    local genes

    if (newMother == nil) then
        return
    end

    if spouse == nil then
        genes = newMother.appearance.genes:new()
        for iteration=0,#genes.appearance-1 do
            genes.appearance[iteration] = pregRng:random(255)
        end
        for iteration=0,#genes.colors-1 do
            genes.colors[iteration] = pregRng:random(32)
        end
    else
        genes = spouse.appearance.genes:new()
    end

    if (newMother.pregnancy_timer > 0) then
        print(dfhack.TranslateName(dfhack.units.getVisibleName(unit)) .. ' is already pregnant!')
        return

    else
        print(dfhack.TranslateName(dfhack.units.getVisibleName(unit)) .. ' is now pregnant!')
    end
    
    newMother.pregnancy_genes = genes;
    newMother.pregnancy_timer = 30;

    if (spouse == nil) then
        newMother.pregnancy_caste = 0;
    else
        newMother.pregnancy_spouse = newMother.relationship_ids[1];
        newMother.pregnancy_caste = 1;
        newMother.pregnancy_spouse = spouse.hist_figure_id
    end

end

function mainScript()
    evalArgs()
    local theList = makeList()
    if #theList == 0 then
        print("No candidates. Nothing done.")
        return
    end
    if doingQuery == 1 then
        local nameList = {}
        for _,unit in pairs(theList) do
            local unitName = dfhack.TranslateName(dfhack.units.getVisibleName(unit))
            table.insert(nameList, unitName)
        end
        table.sort(nameList)
        for _,name in pairs(nameList) do
            print(name)
        end
    else
        for _,unit in pairs(theList) do
            impregnate(unit)
        end
    end
end

dfhack.with_suspend(mainScript)
