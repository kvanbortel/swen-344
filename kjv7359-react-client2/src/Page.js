import { Component } from "react";
import Headings  from "./Headings";
import Controls from './Controls';

class Page extends Component
{
    render()
    {
        return(
            <div>
                <Headings />
                <Controls />
            </div>
        )
    }
}
export default Page;
