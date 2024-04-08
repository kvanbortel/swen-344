import React from 'react';
import {Component} from 'react';

const proteins = {"steak": 300, "ground beef": 200, "chicken": 100, "fish": 80, "soy": 50}
const fruits = {"orange": 300, "banana": 200, "pineapple": 100, "grapes": 80, "blueberries": 50}
const vegetables = {"romaine": 30, "green beans": 40, "squash": 100, "spinach": 50, "kale": 10}
const dairy = {"milk": 300, "yoghurt": 200, "cheddar cheese": 200, "skim milk": 100, "cottage cheese": 80}
const grains = {"bread": 200, "bagel": 300, "pita": 250, "naan": 210, "tortilla": 120}
const foodGroups = {"proteins": proteins, "fruits": fruits, "vegetables": vegetables, "dairy": dairy, "grains": grains}
const allFoods = {...proteins, ...fruits, ...vegetables, ...dairy, ...grains}

let addFoodItem = true
let calorieTotal = 0

class Controls extends Component
{
    constructor(props) {
        super(props)
        this.state = {
            buttonVal: ">>",
            addFoodItem: true,
            groupSelection: this.target,
            options: [],
        };
    }
    
    updateMenu=(e)=>
    {
        const selection = e.target.value
        this.setState({groupSelection: selection, options: Object.keys(foodGroups[selection])})
    }
    buttonAdd=()=>
    {
        this.setState({buttonVal: ">>", addFoodItem: true})
    }
    buttonRemove=()=>
    {
        this.setState({buttonVal: "<<", addFoodItem: false})
    }
    updateSelection()
	{
		alert ("Ouch you clicked me!")
        
	}
    render()
    {
        return(
        <div>
            <div className="flex-container">
                <div>
                    <select onChange={this.updateMenu}>
                        <option value="" selected disabled hidden></option>
                        <option value="proteins">Proteins</option>
                        <option value="fruits">Fruits</option>
                        <option value="vegetables">Vegetables</option>
                        <option value="dairy">Dairy</option>
                        <option value="grains">Grains</option>
                    </select>
                </div>
                <div>
                    <select className="selectBox" size="5" onFocus={this.buttonAdd}>
                        {this.state.options.map(option => <option value={option}>{option}</option>)}
                    </select>
                </div>
                <div>
                    <input type="button" value={this.state.buttonVal} onClick={this.updateSelection}/>
                </div>
                <div>
                    <select className="selectBox" size="10" onFocus={this.buttonRemove}>
                    </select>
                    <label class="hidden" for="selectedItems" id="calorieLabel">Total Calories:</label>
                </div>
            </div>
        </div>
        )
    }
} 

export default Controls;
