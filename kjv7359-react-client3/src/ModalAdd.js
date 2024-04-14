import React from 'react';
import {Component} from 'react';
import {Modal, ModalHeader, ModalBody, ModalFooter, Button, InputGroup, Input, InputGroupText, Row, Col} from 'reactstrap';

class ModalAdd extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            foodName: "",
            foodCalories: "",
            foodTotFat: "",
            foodSatFat: "",
            foodTransFat: "",
            foodProtein: "",
            foodCarbs: ""
        };
    }
    toggle = () =>
    {
        this.props.cancel();
    }

    updateFoodInfo = (e) =>
    {
        //const menuSelection = this.state.selectedMenuItem
        this.setState({
            foodCalories: e.target.value
        });
    }

    saveChanges = () =>
    {
        this.props.callback(this.state.foodCalories);
    }
    render()
    {
  
    return(
        <Modal isOpen={this.props.showHide} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>{this.props.name}</ModalHeader>
        <ModalBody>
            <InputGroup>
                <InputGroupText>Name</InputGroupText>
                <Input onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Calories</InputGroupText>
                <Input placeholder={this.state.foodCalories} onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Total Fat</InputGroupText>
                <Input placeholder={this.state.foodTotFat} onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Saturated Fat</InputGroupText>
                <Input placeholder={this.state.foodSatFat} onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Trans Fat</InputGroupText>
                <Input placeholder={this.state.foodTransFat} onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Protein</InputGroupText>
                <Input placeholder={this.state.foodProtein} onChange={this.updateFoodInfo}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Carbohydrate</InputGroupText>
                <Input placeholder={this.state.foodCarbs} onChange={this.updateFoodInfo}/>
            </InputGroup>
        </ModalBody>
        <ModalFooter>
            <Button color="primary" onClick={this.saveChanges}>Save</Button>
            <Button color="secondary" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>

        </Modal>
        )
    }
}

export default ModalAdd;
