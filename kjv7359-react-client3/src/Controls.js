import React from 'react';
import {Component} from 'react';
import FModal from './FModal';
import IModalTot from './IModalTot';
import {Container, Row, Col, DropdownMenu, DropdownItem, DropdownToggle, Dropdown, Label, Input, Card, CardTitle, CardHeader, ButtonGroup, Button, Progress, Form, FormGroup, ModalHeader, ModalBody, ModalFooter, Modal, InputGroup, InputGroupText} from "reactstrap";
import IModalSingle from './IModalSingle';
import ModalAdd from './ModalAdd';

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
            groupSelection: this.target,
            menuItems: [],
            selectedMenuItem: "",
            foodItems: [],
            selectedFoodId: "",
            calorieTotal: 0,
            dropdownOpen: false,
            calorieGoal: 2000,
            showEditModal: false,
            showTotModal: false,
            showSingleModal: false,
            showAddModal: false
        };
        this.nextFoodItemIndex = 0
    }
    
    updateMenu=(e)=>
    {
        const selection = e.target.value
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

    addSelection=()=>
	{
        let state = {}
        let foodItems = this.state.foodItems
        let calorieTotal = this.state.calorieTotal

        const menuSelection = this.state.selectedMenuItem
        if (menuSelection === "")
            return
        foodItems.push({value: this.nextFoodItemIndex.toString(), text: menuSelection})
        this.nextFoodItemIndex += 1
        calorieTotal += allFoods[menuSelection] // calculate calories

        this.setState({...state, foodItems: foodItems, calorieTotal: calorieTotal})
	}
    removeSelection=()=>
    {
        let state = {}
        let foodItems = this.state.foodItems
        let calorieTotal = this.state.calorieTotal

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

        this.setState({...state, foodItems: foodItems, calorieTotal: calorieTotal})
    }

    changeGoal=(e)=>
    {
        this.setState({calorieGoal: e.target.value})
    }

    showEditItemModal=()=>
    {
        this.setState({showEditModal: true})
    }
    closeEditItemModal=()=>
    {
        this.setState({showEditModal: false})
    }

    showTotItemModal=()=>
    {
        this.setState({showTotModal: true})
    }
    closeTotItemModal=()=>
    {
        this.setState({showTotModal: false})
    }
    showSingleItemModal=()=>
    {
        this.setState({showSingleModal: true})
    }
    closeSingleItemModal=()=>
    {
        this.setState({showSingleModal: false})
    }
    showAddItemModal=()=>
    {
        this.setState({showAddModal: true})
    }
    closeAddItemModal=()=>
    {
        this.setState({showAddModal: false})
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
                            <DropdownItem onClick={this.updateMenu} value="proteins">Proteins</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="fruits">Fruits</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="vegetables">Vegetables</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="dairy">Dairy</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="grains">Grains</DropdownItem>
                        </DropdownMenu>
                    </Dropdown>
                </Col>
                <Col xs="12" md="5" lg="3" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Menu Items</h4></CardHeader>
                        <Input type="select" id="menuItems" size="5" value={this.state.selectedMenuItem} onChange={this.updateMenuSelection}>
                            {this.state.menuItems.map(option => <option value={option} key={option}>{option}</option>)}
                        </Input>
                        <ButtonGroup>
                            <Button color="info" onClick={this.showSingleItemModal}>View Item</Button>
                            <Button color="primary" onClick={this.showAddItemModal}>Add Item</Button>
                            <Button color="secondary" onClick={this.showEditItemModal}>Edit Item</Button>
                        </ButtonGroup>
                        <IModalSingle cancel={this.closeSingleItemModal} showHide={this.state.showSingleModal}></IModalSingle>
                        <ModalAdd callback={this.updateFoodInfo} cancel={this.closeAddItemModal} showHide={this.state.showAddModal}></ModalAdd>
                        <FModal callback={this.updateFoodInfo} cancel={this.closeEditItemModal} showHide={this.state.showEditModal}></FModal>
                    </Card>
                </Col>
                <Col xs="12" md="2" lg="2" className="ptb">
                    <Button color="primary" id="selectButton" onClick={this.addSelection}>Add</Button>
                    {' '}
                    <Button color="primary" id="selectButton" onClick={this.removeSelection}>Remove</Button>
                </Col>
                <Col xs="12" md="5" lg="5" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Selected Items</h4></CardHeader>
                        <Input type="select" id="selectedItems" size="5" value={this.state.selectedFoodId} onChange={this.updateFoodSelection}>
                            {this.state.foodItems.map(option => <option value={option.value} key={option.value}>{option.text}</option>)}
                        </Input>
                        <Button color="info" onClick={this.showTotItemModal}>View Total Item Info</Button>
                        <IModalTot cancel={this.closeTotItemModal} showHide={this.state.showTotModal}></IModalTot>
                        <Label className={this.state.foodItems.length === 0 ? "hidden" : ""} htmlFor="selectedItems">{`Total Calories: ${this.state.calorieTotal}`}</Label>
                    </Card>
                </Col>
                </Row>
                <Row>
                    <Col xs="12" md="12" lg="12" className="ptb">
                    <Card>
                        <CardHeader>
                            <InputGroup>
                                <InputGroupText>Calorie Goal:</InputGroupText>
                                <Input placeholder="2000" onChange={this.changeGoal}/>
                            </InputGroup>
                        </CardHeader>
                            <Progress value={this.state.calorieTotal / this.state.calorieGoal * 100}/>
                    </Card>
                    </Col>
                </Row>
            </Container>
        </div>
        )
    }
} 

export default Controls;
