import React from 'react';
import {Component} from 'react';
import {Modal, ModalHeader, ModalBody, ModalFooter, Button, InputGroup, Input, InputGroupText, Row, Col, Card, ListGroup, ListGroupItem, Badge} from 'reactstrap';

const totCaloriesCap = 2000
const totTotFatCap = 67
const totSatFatCap = 20
const totTransFatCap = 2.2
const totProteinCap = 175
const totCarbsCap = 275

class IModalSingle extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            foodCalories: 0,
            foodTotFat: 0,
            foodSatFat: 0,
            foodTransFat: 0,
            foodProtein: 0,
            foodCarbs: 0,
            healthy: "",
        };
    }
    toggle = () =>
    {
        this.props.cancel();
    }

    render()
    {
  
    return(
        <Modal isOpen={this.props.showHide} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>{this.props.name}</ModalHeader>
        <ModalBody>
            <Card>
                <ListGroup flush>
                    <ListGroupItem color={this.state.healthy}>Calories: {this.state.foodCalories}</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Total Fat: {this.state.foodTotFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Saturated Fat: {this.state.foodSatFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Trans Fat: {this.state.foodTransFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Protein: {this.state.foodProtein}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Carbohydrate: {this.state.foodCarbs}g</ListGroupItem>
                </ListGroup>
            </Card>
        </ModalBody>
        <ModalFooter>
            <Button color="secondary" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
        </Modal>
        )
    }
}

export default IModalSingle;
