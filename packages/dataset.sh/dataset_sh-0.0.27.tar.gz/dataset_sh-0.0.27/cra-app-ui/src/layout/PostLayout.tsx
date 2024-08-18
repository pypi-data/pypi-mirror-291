import React from "react";
import {Outlet} from "react-router-dom";

export function PostLayout() {
    return <div>
        <Outlet/>
    </div>
}