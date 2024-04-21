import { Component } from "react";
import Headings  from "../../kjv7359-react-client4/src/Headings";
import Controls from './Controls';

class Page extends Component
{
    constructor(props)
    {
        super(props)
        this.state = {
            foods: [],
            categories: [],
            foodsByCategory: [],
        }
    }

    updateCategories = (apiResonse) => {
        this.setState({categories: apiResonse})
    }

    updateFoods = (apiResponse) => {
        this.setState({foods: apiResponse})
    }

    updateFoodsByCategory = (apiResponse) => {
        this.setState({foodsbyCategory: apiResponse})
    }

    fetchFoods = () => {
        fetch('http://localhost:5000/foods')
        .then(
            (response) => 
            {
                if (response.status === 200)
                   return (response.json())
                else
                {
                    console.log("HTTP error:" + response.status + ":" +  response.statusText)
                    return ([["status ", response.status]])
                }
            }
        ) //The promise response is returned, then we extract the json data
        .then ((jsonOutput) => //jsonOutput now has result of the data extraction
            {
                this.updateFoods(jsonOutput)
            }
        )
        .catch((error) => 
            {   
                console.log(error)
                this.updateFoods("")
            }
        )
    }

    fetchFoodsByCategory = (category) => {
        fetch('http://localhost:5000/foods?category=' + encodeURIComponent(category))
        .then(
            (response) => 
            {
                if (response.status === 200)
                   return (response.json())
                else
                {
                    console.log("HTTP error:" + response.status + ":" +  response.statusText)
                    return ([["status ", response.status]])
                }
            }
        ) //The promise response is returned, then we extract the json data
        .then ((jsonOutput) => //jsonOutput now has result of the data extraction
            {
                this.updateFoodsByCategory(jsonOutput)
            }
        )
        .catch((error) => 
            {   
                console.log(error)
                this.updateFoodsByCategory("")
            }
        )
    }

    // TODO: make category_id work
    addFood = (name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)=>
    {
        let url = 'http://localhost:5000/foods'
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
        fetch(url,
            {
                method: 'POST',
                body: jData,
                headers: {"Content-type": "application/json; charset=UTF-8"}        
            })
        .then(
            (response) => 
            {
                if (response.status === 200)
                    return (response.json())
                else
                    return ([ ["status ", response.status]])
            }
        )//The promise response is returned, then we extract the json data
        .then ((jsonOutput) => //jsonOutput now has result of the data extraction, but don't need it in this case
            {
                this.fetchFoods()
            }
        )
        .catch((error) => 
            {
                console.log(error)
                this.fetchFoods()
            }
        )
    }

    editFood = (id, name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)=>
    {
        let url = 'https://localhost:5000/foods'
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
        fetch(url,
            {
                method: 'PUT',
                body: jData,
                headers: {"Content-type": "application/json; charset=UTF-8"}
            })
        .then(
            (response) =>
            {
                if(response.status === 200)
                    return (response.json())
                else
                    return ([["status ", response.status]])
            }
        )
        .then((jsonOutput) =>
            {
                this.fetchFoods()
            }
        )
        .catch((error) =>
            {
                console.log(error)
                this.fetchFoods()
            }
        )
    }

    fetchCategories = () => {
        fetch('http://localhost:5000/categories')
        .then(
            (response) => 
            {
                if (response.status === 200)
                   return (response.json())
                else
                {
                    console.log("HTTP error:" + response.status + ":" +  response.statusText)
                    return ([["status ", response.status]])
                }
            }
        ) //The promise response is returned, then we extract the json data
        .then ((jsonOutput) => //jsonOutput now has result of the data extraction
            {
                this.updateCategories(jsonOutput)
            }
        )
        .catch((error) => 
            {   
                console.log(error)
                this.updateCategories("")
            }
        )
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
                <Controls categoriesContent={this.state.categories}
                          foodsByCategoryContent={this.state.foodsByCategory}
                          foodContent={this.state.foods} newFoodContent={this.addFood} editedFoodCallback={this.editFood}
                />
            </div>
        )
    }
}
export default Page;
