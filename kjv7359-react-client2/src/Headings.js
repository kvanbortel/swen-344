import React from 'react';
import {Component} from 'react';

class Headings extends Component
{
    render()
    {
        return(
        <div>
            <div className="flex-container">
                <h1>NutriKit Food Planner</h1>
            </div>
            <div className="flex-container">
                <h3>NutriKit allows you to select your groceries, and track your nutritional progress (good or bad)</h3>
            </div>
        </div>
        )
    }
} 

export default Headings;
