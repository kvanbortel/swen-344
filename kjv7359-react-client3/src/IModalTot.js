import React from 'react';
import {Component} from 'react';
import {Modal, ModalHeader, ModalBody, ModalFooter, Button, InputGroup, Input, InputGroupText, Row, Col, Card, ListGroup, ListGroupItem, Badge} from 'reactstrap';

const totCaloriesCap = 2000
const totTotFatCap = 67
const totSatFatCap = 20
const totTransFatCap = 2.2
const totProteinCap = 175
const totCarbsCap = 275

class IModalTot extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            totFoodCalories: 0,
            totFoodTotFat: 0,
            totFoodSatFat: 0,
            totFoodTransFat: 0,
            totFoodProtein: 0,
            totFoodCarbs: 0,
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
                    <ListGroupItem color={this.state.healthy}>Calories: {this.state.totFoodCalories}</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Total Fat: {this.state.totFoodTotFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Saturated Fat: {this.state.totFoodSatFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Trans Fat: {this.state.totFoodTransFat}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Protein: {this.state.totFoodProtein}g</ListGroupItem>
                    <ListGroupItem color={this.state.healthy}>Carbohydrate: {this.state.totFoodCarbs}g</ListGroupItem>
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

export default IModalTot;
