import React, { Component } from 'react';


class MyComponent extends Component{
    constructor(props){
        super(props);
        this.state={data: ""}
    }

    updateData = (apiResponse) => {
        this.setState({data: apiResponse})
    }

    fetchData = () => {
         fetch('http://localhost:5000/nutrikit_api')
         .then(
             (response) => 
             {
                if (response.status === 200)
                {
                   return (response.json()) ;
                }
                else
                {
                    console.log("HTTP error:" + response.status + ":" +  response.statusText);
                    return ([ ["status ", response.status]]);
                }
             }
             )//The promise response is returned, then we extract the json data
         .then ((jsonOutput) => //jsonOutput now has result of the data extraction
                  {
                      this.updateData(jsonOutput);
                  }
              )
        .catch((error) => 
                {console.log(error);
                    this.updateData("");
                 } )
    
      }


    componentDidMount(){
        this.fetchData();
    }


    render(){
        /*If the data has not yet been loaded from the server, return empty page */
        if ( this.state.data === null || this.state.data === "")
            return (<div><p>No data returned from server</p></div>)
        else
        {
        return (
            <div>
                <div><h2>The api response is: </h2>
                {
                    Object.keys(this.state.data).map(i => 
                            <div>
                               { this.state.data[i].map(x => x + ";" )};
                            </div>
                        )
                }
                </div>
            </div>
        )
        }
    }
}

export default MyComponent;
