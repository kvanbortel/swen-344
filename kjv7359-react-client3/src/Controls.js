import React from 'react';
import {Component} from 'react';
import NutrientsModal from './NutrientsModal';
import {Container, Row, Col, DropdownMenu, DropdownItem, DropdownToggle, Dropdown, Input, Card, CardHeader,
        ButtonGroup, Button, Progress, InputGroup, InputGroupText} from "reactstrap";
import EditFoodModal from './EditFoodModal';
import baseFoodData from './foods.json';

class Controls extends Component
{
    constructor(props) {
        super(props)
        this.nutrientNames = ["calories", "totalFat", "saturatedFat", "transFat", "protein", "carbohydrate"]
        this.state = {
            groupSelection: this.target,
            menuItems: [],
            selectedMenuItem: "",
            foodItems: [],
            foodSelection: "",
            nutrientTotals: Object.fromEntries(this.nutrientNames.map(name => [name, 0])),
            dropdownOpen: false,
            calorieGoal: 2000,
            showEditModal: false,
            showTotModal: false,
            showSingleModal: false,
            showAddModal: false,
            foodData: baseFoodData
        }
        this.nextFoodItemIndex = 0
    }
    
    updateMenu=(e)=>
    {
        const selection = e.target.value
        this.setState({
            groupSelection: selection,
            menuItems: this.state.foodData.filter(food => food.category === selection).map(food => food.id)
        })
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
        this.setState({foodSelection: e.target.value})
    }

    addSelection=()=>
	{
        let foodItems = this.state.foodItems
        let nutrientTotals = this.state.nutrientTotals

        let menuSelection = this.state.selectedMenuItem
        if (menuSelection === "")
            return
        menuSelection = parseInt(menuSelection)
        foodItems.push({key: this.nextFoodItemIndex.toString(), id: menuSelection})
        this.nextFoodItemIndex += 1

        // nutrient totals
        for (const name of this.nutrientNames)
        {
            nutrientTotals[name] += this.state.foodData[menuSelection][name]
        }

        this.setState({foodItems: foodItems, nutrientTotals: nutrientTotals})
	}
    removeSelection=()=>
    {
        let state = {}
        let foodItems = this.state.foodItems
        let nutrientTotals = this.state.nutrientTotals

        const foodSelection = this.state.foodSelection
        if (foodSelection === "")
        {
            console.log("Oh no! There's nothing!")
            return
        }
        const index = foodItems.findIndex(item => item.key === foodSelection)
        console.log(`index=${index} length=${foodItems.length}`)
        const food = this.state.foodData[foodItems[index].id]
        foodItems.splice(index, 1)
        if (foodItems.length === 0)
        {
            state.foodSelection = ""
        }
        else {
            state.foodSelection = foodItems[foodItems.length - 1].key
        }

        // nutrient totals
        for (const name of this.nutrientNames)
        {
            nutrientTotals[name] -= food[name]
        }

        this.setState({...state, foodItems: foodItems, nutrientTotals: nutrientTotals})
    }

    changeGoal=(e)=>
    {
        this.setState({calorieGoal: e.target.value})
    }

    showEditItemModal=(show)=>
    {
        return () => this.setState({showEditModal: show})
    }

    showTotItemModal=(show)=>
    {
        return () => this.setState({showTotModal: show})
    }

    showSingleItemModal=(show)=>
    {
        return () => this.setState({showSingleModal: show})
    }

    showAddItemModal=(show)=>
    {
        return () => this.setState({showAddModal: show})
    }

    getSingleNutrients=()=>
    {
        const menuSelection = this.state.selectedMenuItem
        if (menuSelection === "")
        {
            return null
        }
        return this.state.foodData[parseInt(menuSelection)]
    }

    updateFoodInfo=(data, isEdit)=>
    {
        const name = data.name
        const foodData = this.state.foodData

        if (name === "")
        {
            return false
        }

        if (!isEdit && foodData.find(food => food.name === name) !== null)
        {
            return false
        }

        for (const nutrient of this.nutrientNames)
        {
            data[nutrient] = parseFloat(data[nutrient])
            if (isNaN(data[nutrient]))
            {
                return false
            }
        }

        const newData = {
            id: isEdit ? data.id : foodData.length,
            name: name,
            category: this.state.groupSelection,
            ...data
        }
        
        if (isEdit)
        {
            foodData[data.id] = newData
        }
        else
        {
            foodData.push(newData)
        }
        
        this.setState({foodData: foodData})
        return true
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
                            <DropdownItem onClick={this.updateMenu} value="Proteins">Proteins</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="Fruits">Fruits</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="Vegetables">Vegetables</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="Dairy">Dairy</DropdownItem>
                            <DropdownItem onClick={this.updateMenu} value="Grains">Grains</DropdownItem>
                        </DropdownMenu>
                    </Dropdown>
                </Col>
                <Col xs="12" md="5" lg="3" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Menu Items</h4></CardHeader>
                        <Input type="select" id="menuItems" size="5" value={this.state.selectedMenuItem}
                                onChange={this.updateMenuSelection}>
                            {this.state.menuItems.map(id => this.state.foodData[id])
                                .map(option => <option value={option.id} key={option.id}>{option.name}</option>)}
                        </Input>
                        <ButtonGroup>
                            <Button disabled={this.state.selectedMenuItem === ""} color="info" onClick={this.showSingleItemModal(true)}>View Item</Button>
                            <Button color="primary" onClick={this.showAddItemModal(true)}>Add Item</Button>
                            <Button disabled={this.state.selectedMenuItem === ""} color="secondary" onClick={this.showEditItemModal(true)}>Edit Item</Button>
                        </ButtonGroup>
                        <NutrientsModal cancel={this.showSingleItemModal(false)} showHide={this.state.showSingleModal}
                            data={this.getSingleNutrients()}></NutrientsModal>
                        <EditFoodModal callback={this.updateFoodInfo} cancel={this.showAddItemModal(false)}
                            showHide={this.state.showAddModal}></EditFoodModal>
                        <EditFoodModal callback={this.updateFoodInfo} cancel={this.showEditItemModal(false)}
                            showHide={this.state.showEditModal} data={this.getSingleNutrients()}></EditFoodModal>
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
                        <Input type="select" id="selectedItems" size="5" value={this.state.foodSelection}
                                onChange={this.updateFoodSelection}>
                            {this.state.foodItems.map(option =>
                                <option value={option.key} key={option.key}>
                                    {this.state.foodData[option.id].name}
                                </option>
                            )}
                        </Input>
                        <Button color="info" onClick={this.showTotItemModal(true)}>View Total Item Info</Button>
                        <NutrientsModal cancel={this.showTotItemModal(false)} showHide={this.state.showTotModal}
                            data={this.state.nutrientTotals}></NutrientsModal>
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
                            <Progress value={this.state.nutrientTotals.calories / this.state.calorieGoal * 100}/>
                    </Card>
                    </Col>
                </Row>
            </Container>
        </div>
        )
    }
} 

export default Controls;
