import React from 'react';
import {Component} from 'react';
import NutrientsModal from '../../kjv7359-react-client4/src/NutrientsModal';
import {Container, Row, Col, DropdownMenu, DropdownItem, DropdownToggle, Dropdown, Input, Card, CardHeader,
        ButtonGroup, Button, Progress, InputGroup, InputGroupText} from "reactstrap";
import EditFoodModal from '../../kjv7359-react-client4/src/EditFoodModal';

class Controls extends Component
{
    constructor(props) {
        super(props)
        this.nutrientNames = ["calories", "totalFat", "saturatedFat", "transFat", "protein", "carbohydrate"]
        this.state = {
            groupSelection: "",
            menuItems: [],
            selectedMenuItem: "",
            foodItems: [],
            foodSelection: "",
            dropdownOpen: false,
            calorieGoal: 2000,
            showEditModal: false,
            showTotModal: false,
            showSingleModal: false,
            showAddModal: false,
        }
        this.nextFoodItemIndex = 0
    }
    
    getFoodById=(id)=>
    {
        return this.props.foods.find(food => food.id === id)
    }

    updateMenu=(e)=>
    {
        this.setState({groupSelection: e.target.value})
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

        // this would work better with getElementByID since ReactStrap doesn't fire onChange
        // when the contents change the selection, but I was advised to put it back without default selection
        let menuSelection = this.state.selectedMenuItem
        if (menuSelection === "")
            return
        menuSelection = parseInt(menuSelection)
        foodItems.push({key: this.nextFoodItemIndex.toString(), id: menuSelection})
        this.nextFoodItemIndex += 1

        this.setState({foodItems: foodItems})
    }
    removeSelection=()=>
    {
        let state = {}
        let foodItems = this.state.foodItems

        // this would work better with getElementByID since ReactStrap doesn't fire onChange
        // when the contents change the selection, but I was advised to put it back without default selection
        const foodSelection = this.state.foodSelection
        if (foodSelection === "")
            return
        const index = foodItems.findIndex(item => item.key === foodSelection)
        foodItems.splice(index, 1)
        if (foodItems.length === 0)
        {
            state.foodSelection = ""
        }
        else {
            state.foodSelection = foodItems[foodItems.length - 1].key
        }

        this.setState({...state, foodItems: foodItems})
    }

    getNutrientTotals=()=>
    {
        const nutrientTotals = Object.fromEntries(this.nutrientNames.map(name => [name, 0]))
        if (this.props.foods === null || this.props.foods.length === 0)
            return nutrientTotals
        let foodItems = this.state.foodItems
        for(const item of foodItems)
        {
            for (const name of this.nutrientNames)
            {
                nutrientTotals[name] += this.getFoodById(item.id)[name]
            }
        }
        return nutrientTotals
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
        // this would work better with getElementByID since ReactStrap doesn't fire onChange
        // when the contents change the selection, but I was advised to put it back without default selection
        const menuSelection = this.state.selectedMenuItem
        if (menuSelection === "")
        {
            return null
        }
        return this.getFoodById(parseInt(menuSelection))
    }

    updateFoodInfo=(data, isEdit)=>
    {
        data = Object.assign({}, data)

        if (data.name === "")
            return false

        if (!isEdit && this.props.foods.some(food => food.name === data.name))
            return false

        for (const nutrient of this.nutrientNames)
        {
            data[nutrient] = parseFloat(data[nutrient])
            if (!isFinite(data[nutrient]) || data[nutrient] < 0)
            {
                return false
            }
        }
        
        if (isEdit)
        {
            delete data.name
            this.props.editFood(data)
        }
        else
        {
            data.category_id = parseInt(this.state.groupSelection)
            this.props.addFood(data)
        }

        return true
    }


    processCategories = () =>
    {
        if (this.props.categories === null)
        {
            console.log("Empty content");
            return (<DropdownItem>No content</DropdownItem>)
        }
        return(
            this.props.categories.map(cat => 
                <DropdownItem onClick={this.updateMenu} key={cat.id} value={cat.id}>{cat.name}</DropdownItem>
            )
        )
    }

    processFoods = () =>
    {
        if (this.props.foods === null)
        {
            console.log("Empty content");
            return (<option key="">No content</option>)
        }
        if (this.state.groupSelection === "")
        {
            return null
        }
        const category_id = parseInt(this.state.groupSelection)
        return(
            this.props.foods.filter(food => food.category_id === category_id).map(food =>
                <option value={food.id} key={food.id}>{food.name}</option>
            )
        )
    }



    render()
    {
        const nutrientTotals = this.getNutrientTotals()
        return(
        <div>
            <Container className="pt">
                <Row>
                <Col xs="12" md="12" lg="2" className="ptb">
                    <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggleDropdown}>
                        <DropdownToggle caret>Categories</DropdownToggle>
                        <DropdownMenu id="foodGroups">
                            {this.processCategories()}
                        </DropdownMenu>
                    </Dropdown>
                </Col>
                <Col xs="12" md="5" lg="3" className="ptb">
                    <Card>
                        <CardHeader><h4 className="text-center">Menu Items</h4></CardHeader>
                        <Input type="select" id="menuItems" size="5" value={this.state.selectedMenuItem}
                                onChange={this.updateMenuSelection}>
                            {this.processFoods()}
                        </Input>
                        <ButtonGroup>
                            <Button disabled={this.state.selectedMenuItem === ""} color="info"
                                onClick={this.showSingleItemModal(true)}>View Item</Button>
                            <Button disabled={this.state.selectedMenuItem === ""} color="primary"
                                onClick={this.showAddItemModal(true)}>Add Item</Button>
                            <Button disabled={this.state.selectedMenuItem === ""} color="secondary"
                                onClick={this.showEditItemModal(true)}>Edit Item</Button>
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
                                    {this.getFoodById(option.id).name}
                                </option>
                            )}
                        </Input>
                        <Button color="info" onClick={this.showTotItemModal(true)}>View Total Item Info</Button>
                        <NutrientsModal cancel={this.showTotItemModal(false)} showHide={this.state.showTotModal}
                            data={nutrientTotals}></NutrientsModal>
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
                            <Progress color={nutrientTotals.calories > this.state.calorieGoal ? "danger" : ""}
                                value={nutrientTotals.calories / this.state.calorieGoal * 100}/>
                    </Card>
                    </Col>
                </Row>
            </Container>
        </div>
        )
    }
} 

export default Controls;
