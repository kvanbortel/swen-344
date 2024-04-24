import React from 'react'
import {Component} from 'react'
import {Modal, ModalHeader, ModalBody, ModalFooter, Button, Card, ListGroup, ListGroupItem} from 'reactstrap'

const dailyMaximums = {calories: 2000, totalFat: 67, saturatedFat: 20, transFat: 2.2, protein: 175, carbohydrate: 275}

class NutrientsModal extends Component
{
    close = () =>
    {
        this.props.cancel()
    }

    getColor=(name)=>
    {
        if (this.props.data !== null && this.props.data[name] > dailyMaximums[name])
        {
            return "danger"
        }
        return ""
    }

    render()
    {
        const data = this.props.data ?? Object.fromEntries(Object.keys(dailyMaximums).map(name => [name, 0]))

        return (
            <Modal isOpen={this.props.showHide} toggle={this.close}>
            <ModalHeader toggle={this.close}>{data.name ?? ""}</ModalHeader>
            <ModalBody>
                <Card>
                    <ListGroup flush>
                        <ListGroupItem color={this.getColor("calories")}>Calories: {data.calories.toFixed(2)}</ListGroupItem>
                        <ListGroupItem color={this.getColor("totalFat")}>Total Fat: {data.totalFat.toFixed(2)}g</ListGroupItem>
                        <ListGroupItem color={this.getColor("saturatedFat")}>Saturated Fat: {data.saturatedFat.toFixed(2)}g</ListGroupItem>
                        <ListGroupItem color={this.getColor("transFat")}>Trans Fat: {data.transFat.toFixed(2)}g</ListGroupItem>
                        <ListGroupItem color={this.getColor("protein")}>Protein: {data.protein.toFixed(2)}g</ListGroupItem>
                        <ListGroupItem color={this.getColor("carbohydrate")}>Carbohydrate: {data.carbohydrate.toFixed(2)}g</ListGroupItem>
                    </ListGroup>
                </Card>
            </ModalBody>
            <ModalFooter>
                <Button color="secondary" onClick={this.close}>Cancel</Button>
            </ModalFooter>
            </Modal>
        )
    }
}

export default NutrientsModal
