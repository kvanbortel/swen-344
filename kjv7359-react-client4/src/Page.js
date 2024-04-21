import { Component } from "react";
import Headings  from "../../kjv7359-react-client4/src/Headings";
import Controls from './Controls';

const baseURL = 'http://localhost:5000'

class Page extends Component
{
    constructor(props)
    {
        super(props)
        this.state = {
            foods: [],
            categories: [],
        }
    }

    handleResponse = (promise, callback) => {
        promise.then(response => {
            if (response.status === 200)
                response.json().then(callback)
            else
                console.log("HTTP error:" + response.status + ":" +  response.statusText)
        })
        .catch((error) => {   
            console.log(error)
        })
    }

    fetchFoods = () => {
        let url = baseURL + '/foods'
        const promise = fetch(url)
        this.handleResponse(promise, apiResponse => this.setState({foods: apiResponse}))
    }

    // TODO: make category_id work
    addFood = (name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)=>
    {
        let url = baseURL + '/foods'
        let jData = JSON.stringify({
            name: name,
            category_id: category_id,
            calories: calories,
            totalFat: totalFat,
            saturatedFat: saturatedFat,
            transFat: transFat,
            protein: protein,
            carbohydrate: carbohydrate,
            })
        const promise = fetch(url,
            {
                method: 'POST',
                body: jData,
                headers: {"Content-type": "application/json; charset=UTF-8"}        
            })
        this.handleResponse(promise, response => this.fetchFoods({}))
    }

    editFood = (id, name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)=>
    {
        let url = baseURL + '/foods'
        let jData = JSON.stringify({
            id: id,
            name: name,
            category_id: category_id,
            calories: calories,
            totalFat: totalFat,
            saturatedFat: saturatedFat,
            transFat: transFat,
            protein: protein,
            carbohydrate: carbohydrate,
        })
        const promise = fetch(url,
            {
                method: 'PUT',
                body: jData,
                headers: {"Content-type": "application/json; charset=UTF-8"}
            })
        this.handleResponse(promise, response => this.fetchFoods())
    }

    fetchCategories = () => {
        let url = baseURL + '/categories'
        const promise = fetch(url)
        this.handleResponse(promise, apiResponse => {
            this.setState({categories: apiResponse})
        })
    }

    componentDidMount()
    {
        this.fetchFoods()
        this.fetchCategories()
    }

    render()
    {
        return(
            <div>
                <Headings />
                <Controls categories={this.state.categories}
                          foods={this.state.foods}
                          addFood={this.addFood} editFood={this.editFood}
                />
            </div>
        )
    }
}
export default Page;
