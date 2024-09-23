import React from 'react'
import {Component} from 'react'
import NutrientsModal from '../../kjv7359-react-client4/src/NutrientsModal'
import {Container, Row, Col, DropdownMenu, DropdownItem, DropdownToggle, Dropdown, Input, Card, CardHeader,
        ButtonGroup, Button, Progress, InputGroup, InputGroupText} from "reactstrap"
import EditFoodModal from '../../kjv7359-react-client4/src/EditFoodModal'
import DeleteModal from './DeleteModal'

class Controls extends Component
{
    constructor(props) {
        super(props)
        this.nutrientNames = ["calories", "totalFat", "saturatedFat", "transFat", "protein", "carbohydrate"]
        this.state = {
            groupSelection: null,
            menuItems: [],
            selectedMenuItem: null,
            foodItems: [],
            foodSelection: "",
            dropdownOpen: false,
            calorieGoal: 2000,
            showEditModal: false,
            showDeleteModal: false,
            showTotModal: false,
            showSingleModal: false,
            showAddModal: false,
        }
        this.nextFoodItemIndex = 0
    }
    
    getFoodById = (id) =>
    {
        return this.props.foods.find(food => food.id === id)
    }

    updateMenu = (e) =>
    {
        const value = e.target.value
        this.setState({groupSelection: value === "" ? null : parseInt(value)})
    }
    toggleDropdown = () =>
    {
        this.setState({dropdownOpen: !this.state.dropdownOpen})
    }

    updateMenuSelection = (e) =>
    {
        const value = e.target.value
        this.setState({selectedMenuItem: value === "" ? null : parseInt(value)})
    }
    updateFoodSelection = (e) =>
    {
        this.setState({foodSelection: e.target.value})
    }

    addSelection = () =>
    {
        let foodItems = this.state.foodItems

        let menuSelection = this.state.selectedMenuItem
        if (menuSelection === null)
            return
        foodItems.push({key: this.nextFoodItemIndex.toString(), id: menuSelection})
        this.nextFoodItemIndex += 1

        this.setState({foodItems: foodItems})
    }
    removeSelection = () =>
    {
        let state = {}
        let foodItems = this.state.foodItems

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

    getNutrientTotals = () =>
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

    changeGoal = (e) =>
    {
        this.setState({calorieGoal: e.target.value})
    }

    showDeleteItemModal = (show) =>
    {
        return () => this.setState({showDeleteModal: show})
    }

    showEditItemModal = (show) =>
    {
        return () => this.setState({showEditModal: show})
    }

    showTotItemModal = (show) =>
    {
        return () => this.setState({showTotModal: show})
    }

    showSingleItemModal = (show) =>
    {
        return () => this.setState({showSingleModal: show})
    }

    showAddItemModal = (show) =>
    {
        return () => this.setState({showAddModal: show})
    }

    getSingleNutrients = () =>
    {
        const menuSelection = this.state.selectedMenuItem
        return menuSelection === null ? null : this.getFoodById(menuSelection)
    }

    updateFoodInfo = (data, isEdit) =>
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
            data.category_id = this.state.groupSelection
            this.props.addFood(data)
        }

        return true
    }

    deleteCleanup = (newFoods) =>
    {
        const newIds = new Set(newFoods.map(food => food.id))
        const foodItems = this.state.foodItems.filter(item => newIds.has(item.id))
        const firstMenuMatch = newFoods.find(
            food => food.category_id === this.state.groupSelection)
        const newMenuSelection = firstMenuMatch === undefined ? null : firstMenuMatch.id
        const newFoodSelection = foodItems.length === 0 ? "" : foodItems[0].key
        this.setState({selectedMenuItem: newMenuSelection, foodSelection: newFoodSelection, foodItems: foodItems})
    }

    deleteItem = () =>
    {
        this.props.deleteFood(this.state.selectedMenuItem, this.deleteCleanup)
    }

    processCategories = () =>
    {
        if (this.props.categories === null)
        {
            console.log("Empty content")
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
            console.log("Empty content")
            return (<option key="">No content</option>)
        }
        if (this.state.groupSelection === null)
        {
            return null
        }
        const category_id = this.state.groupSelection
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
                        <Input type="select" id="menuItems" size="5" value={this.state.selectedMenuItem ?? ""}
                                onChange={this.updateMenuSelection}>
                            {this.processFoods()}
                        </Input>
                        <ButtonGroup>
                            <Button disabled={this.state.selectedMenuItem === null} color="info"
                                onClick={this.showSingleItemModal(true)}>View</Button>
                            <Button disabled={this.state.selectedMenuItem === null} color="primary"
                                onClick={this.showAddItemModal(true)}>Add</Button>
                            <Button disabled={this.state.selectedMenuItem === null} color="secondary"
                                onClick={this.showEditItemModal(true)}>Edit</Button>
                            <Button disabled={this.state.selectedMenuItem === null} color="danger"
                                onClick={this.showDeleteItemModal(true)}>Delete</Button>
                        </ButtonGroup>
                        <NutrientsModal cancel={this.showSingleItemModal(false)} showHide={this.state.showSingleModal}
                            data={this.getSingleNutrients()}></NutrientsModal>
                        <EditFoodModal callback={this.updateFoodInfo} cancel={this.showAddItemModal(false)}
                            showHide={this.state.showAddModal}></EditFoodModal>
                        <EditFoodModal callback={this.updateFoodInfo} cancel={this.showEditItemModal(false)}
                            showHide={this.state.showEditModal} data={this.getSingleNutrients()}></EditFoodModal>
                        <DeleteModal callback={this.deleteItem} cancel={this.showDeleteItemModal(false)}
                            showHide={this.state.showDeleteModal}
                            name={this.state.selectedMenuItem ?
                                this.getFoodById(this.state.selectedMenuItem).name : ""}></DeleteModal>
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

export default Controls
