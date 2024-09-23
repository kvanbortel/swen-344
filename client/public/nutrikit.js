const proteins = {"steak": 300, "ground beef": 200, "chicken": 100, "fish": 80, "soy": 50}
const fruits = {"orange": 300, "banana": 200, "pineapple": 100, "grapes": 80, "blueberries": 50}
const vegetables = {"romaine": 30, "green beans": 40, "squash": 100, "spinach": 50, "kale": 10}
const dairy = {"milk": 300, "yoghurt": 200, "cheddar cheese": 200, "skim milk": 100, "cottage cheese": 80}
const grains = {"bread": 200, "bagel": 300, "pita": 250, "naan": 210, "tortilla": 120}
const foodGroups = {"proteins": proteins, "fruits": fruits, "vegetables": vegetables, "dairy": dairy, "grains": grains}
const allFoods = {...proteins, ...fruits, ...vegetables, ...dairy, ...grains}

let addFoodItem = true
let calorieTotal = 0


function updateMenu() {
    document.getElementById("menuItems").innerHTML = ""
    const foodGroup = document.getElementById("foodGroups")
    const selection = foodGroup.options[foodGroup.selectedIndex].value
    const menuItems = document.getElementById("menuItems")

    for (const key in foodGroups[selection]) {
        const option_elem = document.createElement("option")
        option_elem.textContent = key
        menuItems.appendChild(option_elem)
    }
}

function buttonAdd() {
    const button = document.getElementById("selectButton")
    button.value = ">>"
    addFoodItem = true
}

function buttonRemove() {
    const button = document.getElementById("selectButton")
    button.value = "<<"
    addFoodItem = false
}

function updateSelection() {
    const food = document.getElementById("menuItems") 
    const selectedItems = document.getElementById("selectedItems")

    // add selection
    if (addFoodItem) {
        if (food.selectedIndex === -1)
            return
        const menuSelection = food.options[food.selectedIndex].value
        const option_elem = document.createElement("option")
        option_elem.textContent = menuSelection
        selectedItems.appendChild(option_elem)
        // calculate calories
        calorieTotal += allFoods[menuSelection]
    }
    // remove selection
    else {
        if (selectedItems.selectedIndex === -1)
            return
        const itemSelection = selectedItems.options[selectedItems.selectedIndex]
        selectedItems.removeChild(itemSelection)
        // calculate calories
        calorieTotal -= allFoods[itemSelection.value]
        // select bottom
        selectedItems.selectedIndex = selectedItems.length - 1
    }

    // update calorie label
    const label = document.getElementById("calorieLabel")
    if (selectedItems.length === 0)
        label.classList.add("hidden")
    else
        label.classList.remove("hidden")
    label.textContent = `Total Calories: ${calorieTotal}`
}
