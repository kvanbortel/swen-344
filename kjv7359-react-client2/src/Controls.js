import React from 'react';
import {Component} from 'react';

const proteins = {"steak": 300, "ground beef": 200, "chicken": 100, "fish": 80, "soy": 50}
const fruits = {"orange": 300, "banana": 200, "pineapple": 100, "grapes": 80, "blueberries": 50}
const vegetables = {"romaine": 30, "green beans": 40, "squash": 100, "spinach": 50, "kale": 10}
const dairy = {"milk": 300, "yoghurt": 200, "cheddar cheese": 200, "skim milk": 100, "cottage cheese": 80}
const grains = {"bread": 200, "bagel": 300, "pita": 250, "naan": 210, "tortilla": 120}
const foodGroups = {"proteins": proteins, "fruits": fruits, "vegetables": vegetables, "dairy": dairy, "grains": grains}
const allFoods = {...proteins, ...fruits, ...vegetables, ...dairy, ...grains}


class Controls extends Component
{
    constructor(props) {
        super(props)
        this.state = {
            addFoodItem: true,
            groupSelection: this.target,
            menuItems: [],
            selectedMenuItem: "",
            foodItems: [],
            selectedFoodId: "",
            calorieTotal: 0
        };
        this.nextFoodItemIndex = 0
    }
    
    updateMenu=(e)=>
    {
        const selection = e.target.value
        this.setState({groupSelection: selection, menuItems: Object.keys(foodGroups[selection])})
    }
    updateMenuSelection=(e)=>
    {
        this.setState({selectedMenuItem: e.target.value})
    }
    updateFoodSelection=(e)=>
    {
        this.setState({selectedFoodId: e.target.value})
    }
    setDirection=(addFoodItem)=>
    {
        return () => this.setState({addFoodItem: addFoodItem})
    }
    updateSelection=()=>
	{
        let state = {}
        let foodItems = this.state.foodItems
        let calorieTotal = this.state.calorieTotal
        if (this.state.addFoodItem) { // add selection
            const menuSelection = this.state.selectedMenuItem
            if (menuSelection === "")
                return
            foodItems.push({value: this.nextFoodItemIndex.toString(), text: menuSelection})
            this.nextFoodItemIndex += 1
            calorieTotal += allFoods[menuSelection] // calculate calories
        }
        else { // remove selection
            const foodSelection = this.state.selectedFoodId
            if (foodSelection === "")
                return
            const index = foodItems.findIndex(item => item.value === foodSelection)
            const foodName = foodItems[index].text
            foodItems.splice(index, 1)
            if (foodItems.length === 0)
            {
                state.selectedFoodId = ""
            }
            else {
                state.selectedFoodId = foodItems[foodItems.length - 1].value
            }
            calorieTotal -= allFoods[foodName]
        }
        this.setState({...state, foodItems: foodItems, calorieTotal: calorieTotal})
	}
    render()
    {
        return(
        <div>
            <div className="flex-container">
                <div>
                    <label htmlFor="foodGroups">Categories</label>
                    <select id="foodGroups" onChange={this.updateMenu} defaultValue="">
                        <option value="" disabled hidden></option>
                        <option value="proteins">Proteins</option>
                        <option value="fruits">Fruits</option>
                        <option value="vegetables">Vegetables</option>
                        <option value="dairy">Dairy</option>
                        <option value="grains">Grains</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="menuItems">Menu Items</label>
                    <select className="selectBox" id="menuItems" size="5" value={this.state.selectedMenuItem} onChange={this.updateMenuSelection} onFocus={this.setDirection(true)}>
                        {this.state.menuItems.map(option => <option value={option} key={option}>{option}</option>)}
                    </select>
                </div>
                <div>
                    <label htmlFor="selectButton"><br/></label>
                    <input type="button" id="selectButton" value={this.state.addFoodItem ? ">>" : "<<"} onClick={this.updateSelection}/>
                </div>
                <div>
                    <label htmlFor="selectedItems">Selected Items</label>
                    <select className="selectBox" id="selectedItems" size="10" value={this.state.selectedFoodId} onChange={this.updateFoodSelection} onFocus={this.setDirection(false)}>
                        {this.state.foodItems.map(option => <option value={option.value} key={option.value}>{option.text}</option>)}
                    </select>
                    <label className={this.state.foodItems.length === 0 ? "hidden" : ""} htmlFor="selectedItems">{`Total Calories: ${this.state.calorieTotal}`}</label>
                </div>
            </div>
        </div>
        )
    }
} 

export default Controls;
