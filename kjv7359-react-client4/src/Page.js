import { Component } from "react"
import Headings  from "../../kjv7359-react-client4/src/Headings"
import Controls from './Controls'

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

    fetchFoods = (args) => {
        const promise = fetch(baseURL + '/foods')
        this.handleResponse(promise, apiResponse => {
            if ('deleteCleanup' in args)
                args.deleteCleanup(apiResponse)
            this.setState({foods: apiResponse})
        })
    }

    addFood = (params) => // name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate
    {
        const promise = fetch(baseURL + '/foods',
            {
                method: 'POST',
                body: JSON.stringify(params),
                headers: {"Content-type": "application/json; charset=UTF-8"}
            })
        this.handleResponse(promise, response => this.fetchFoods({}))
    }

    editFood = (params) => // id, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate
    {
        const promise = fetch(baseURL + '/foods',
            {
                method: 'PUT',
                body: JSON.stringify(params),
                headers: {"Content-type": "application/json; charset=UTF-8"}
            })
        this.handleResponse(promise, response => this.fetchFoods({}))
    }

    deleteFood = (id, deleteCleanup) =>
    {
        const promise = fetch(baseURL + '/foods?id=' + encodeURI(id),
            {
                method: 'DELETE',
            })
        this.handleResponse(promise, response => this.fetchFoods({deleteCleanup: deleteCleanup}))
    }

    fetchCategories = () => {
        const promise = fetch(baseURL + '/categories')
        this.handleResponse(promise, apiResponse => {
            this.setState({categories: apiResponse})
        })
    }

    componentDidMount()
    {
        this.fetchFoods({})
        this.fetchCategories()
    }

    render()
    {
        return (
            <div>
                <Headings />
                <Controls categories={this.state.categories}
                          foods={this.state.foods}
                          addFood={this.addFood} editFood={this.editFood} deleteFood={this.deleteFood}
                />
            </div>
        )
    }
}
export default Page
