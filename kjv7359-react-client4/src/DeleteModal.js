import React from 'react'
import {Component} from 'react'
import {Modal, ModalHeader, ModalBody, ModalFooter, Button} from 'reactstrap'

class DeleteModal extends Component
{
    close = () =>
    {
        this.props.cancel()
    }

    delete = () =>
    {
        this.props.callback()
        this.close()
    }

    render()
    {

        return (
            <Modal isOpen={this.props.showHide} toggle={this.close}>
            <ModalHeader toggle={this.close}>{this.props.name}</ModalHeader>
            <ModalBody>Are you sure you want to delete this item?</ModalBody>
            <ModalFooter>
                <Button color="danger" onClick={this.delete}>Delete</Button>
                <Button color="secondary" onClick={this.close}>Cancel</Button>
            </ModalFooter>
            </Modal>
        )
    }
}

export default DeleteModal
