import React from 'react';
import {Component} from 'react';
import {Container, Row, Col, DropdownMenu, DropdownItem, DropdownToggle, Dropdown, Label, Input, Card, CardTitle, CardHeader} from "reactstrap";
require('react-dom');
window.React2 = require('react');
console.log(window.React1 === window.React2);

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
            calorieTotal: 0,
            dropdownOpen: false
        };
        this.nextFoodItemIndex = 0
    }
    
    updateMenu=(e)=>
    {
        const selection = e
        this.setState({groupSelection: selection, menuItems: Object.keys(foodGroups[selection])})
    }
    toggleDropdown=()=>
    {
        this.setState({dropdownOpen: !this.state.dropdownOpen})
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
            <Container className="pt">
                <Row>
                <Col xs="12" md="12" lg="2" className="ptb">
                    <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggleDropdown}>
                        <DropdownToggle caret>Categories</DropdownToggle>
                        <DropdownMenu id="foodGroups">
                            <DropdownItem onClick={() => this.updateMenu(proteins)} value="proteins">Proteins</DropdownItem>
                            <DropdownItem onClick={() => this.updateMenu(fruits)} value="fruits">Fruits</DropdownItem>
                            <DropdownItem onClick={() => this.updateMenu(vegetables)} value="vegetables">Vegetables</DropdownItem>
                            <DropdownItem onClick={() => this.updateMenu(dairy)} value="dairy">Dairy</DropdownItem>
                            <DropdownItem onClick={() => this.updateMenu(grains)} value="grains">Grains</DropdownItem>
                        </DropdownMenu>
                    </Dropdown>
                </Col>
                <Col xs="12" md="5" lg="3" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Menu Items</h4></CardHeader>
                        <Input type="select" id="menuItems" size="5" value={this.state.selectedMenuItem} onChange={this.updateMenuSelection} onFocus={this.setDirection(true)}>
                            {this.state.menuItems.map(option => <option value={option} key={option}>{option}</option>)}
                        </Input>
                    </Card>
                </Col>
                <Col xs="6" md="1" lg="1" className="ptb">
                    <input type="button" id="selectButton" value="<<" onClick={this.updateSelection}/>
                </Col>
                <Col xs="6" md="1" lg="1" className="ptb">
                    <input type="button" id="selectButton" value=">>" onClick={this.updateSelection}/>
                </Col>
                <Col xs="12" md="5" lg="5" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Selected Items</h4></CardHeader>
                        <Input type="select" id="selectedItems" size="10" value={this.state.selectedFoodId} onChange={this.updateFoodSelection} onFocus={this.setDirection(false)}>
                            {this.state.foodItems.map(option => <option value={option.value} key={option.value}>{option.text}</option>)}
                        </Input>
                        <Label className={this.state.foodItems.length === 0 ? "hidden" : ""} htmlFor="selectedItems">{`Total Calories: ${this.state.calorieTotal}`}</Label>
                    </Card>
                </Col>
                </Row>
            </Container>
        </div>
        )
    }
} 

export default Controls;
