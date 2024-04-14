import React from 'react';
import {Component} from 'react';
import {Modal, ModalHeader, ModalBody, ModalFooter, Button, InputGroup, Input, InputGroupText} from 'reactstrap';

class EditFoodModal extends Component
{
    constructor(props)
    {
        super(props);
        this.isEdit = "data" in props
        this.state = {
            data: {}
        };
    }
    close = () =>
    {
        this.props.cancel();
    }

    saveChanges = () =>
    {
        const result = this.props.callback(this.state.data, this.isEdit);
        
        if (result)
        {
            this.close()
        }
    }

    handleOpened=()=>
    {
        this.setState({
            data: this.isEdit ? this.props.data :
                {name: "", calories: 0, totalFat: 0, saturatedFat: 0, transFat: 0, protein: 0, carbohydrate: 0}
        })
    }

    updateFoodInfo=(name)=>
    {
        return e =>
        {
            const data = this.state.data
            data[name] = e.target.value
            this.setState({data: data})
        }
    }

    render()
    {
  
    return(
        <Modal isOpen={this.props.showHide} toggle={this.close} onOpened={this.handleOpened}>
        <ModalHeader toggle={this.close}>{this.state.data.name}</ModalHeader>
        <ModalBody>
            <InputGroup>
                <InputGroupText>Name</InputGroupText>
                <Input disabled={this.isEdit} placeholder={this.state.data.name} onChange={this.updateFoodInfo("name")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Calories</InputGroupText>
                <Input placeholder={this.state.data.calories} onChange={this.updateFoodInfo("calories")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Total Fat</InputGroupText>
                <Input placeholder={this.state.data.totalFat} onChange={this.updateFoodInfo("totalFat")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Saturated Fat</InputGroupText>
                <Input placeholder={this.state.data.saturatedFat} onChange={this.updateFoodInfo("saturatedFat")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Trans Fat</InputGroupText>
                <Input placeholder={this.state.data.transFat} onChange={this.updateFoodInfo("transFat")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Protein</InputGroupText>
                <Input placeholder={this.state.data.protein} onChange={this.updateFoodInfo("protein")}/>
            </InputGroup>
            <InputGroup>
                <InputGroupText>Carbohydrate</InputGroupText>
                <Input placeholder={this.state.data.carbohydrate} onChange={this.updateFoodInfo("carbohydrate")}/>
            </InputGroup>
        </ModalBody>
        <ModalFooter>
            <Button color="primary" onClick={this.saveChanges}>Save</Button>
            <Button color="secondary" onClick={this.close}>Cancel</Button>
        </ModalFooter>

        </Modal>
        )
    }
}

export default EditFoodModal;
