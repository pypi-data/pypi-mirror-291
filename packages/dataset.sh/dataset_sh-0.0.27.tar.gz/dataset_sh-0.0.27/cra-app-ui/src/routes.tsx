import React from "react";
import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {MainAppLayout} from "./layout/MainAppLayout";
import {DatasetListingPage} from "./pages/DatasetListingPage";
import {DatasetSamplePage} from "./pages/dataset/DatasetSamplePage";
import {DatasetLayout} from "./layout/DatasetLayout";
import {DatasetMetaPage} from "./pages/dataset/DatasetMetaPage";
import {SingleStoreListingPage} from "./pages/SingleStoreListingPage";
import LoginPage from "./pages/LoginPage";
import {HomePage} from "./pages/HomePage";
import {PostListingPage} from "./pages/post/PostListingPage";
import {PostViewingPage} from "./pages/post/PostViewingPage";
import {DatasetVersionListingPage} from "./pages/dataset/byVersion/DatasetVersionListingPage";
import {DatasetMetaByVersionPage} from "./pages/dataset/byVersion/DatasetMetaByVersionPage";
import {DatasetSampleByVersionPage} from "./pages/dataset/byVersion/DatasetSampleByVersionPage";
import {DatasetMetaByTagPage} from "./pages/dataset/byTag/DatasetMetaByTagPage";
import {DatasetSampleByTagPage} from "./pages/dataset/byTag/DatasetSampleByTagPage";

export function AppRoutes() {
    return <BrowserRouter>
        <Routes>
            <Route element={<MainAppLayout/>}>
                <Route index element={<HomePage/>}/>
                <Route path="/login" element={<LoginPage/>}/>

                <Route path="/post" element={<PostListingPage/>}/>
                <Route path="/post/:postName" element={<PostViewingPage/>}/>

                <Route path="/dataset" element={<DatasetListingPage/>}/>
                <Route path="/dataset/:namespace" element={<SingleStoreListingPage/>}/>

                <Route element={<DatasetLayout/>}>
                    <Route path="/dataset/:namespace/:datasetName" element={<DatasetMetaPage/>}/>
                    <Route path="/dataset/:namespace/:datasetName/collection/:collName"
                           element={<DatasetSamplePage/>}/>
                    <Route path="/dataset/:namespace/:datasetName/tag/:tag" element={<DatasetMetaByTagPage/>}/>
                    <Route path="/dataset/:namespace/:datasetName/tag/:tag/collection/:collName"
                           element={<DatasetSampleByTagPage/>}/>

                    <Route path="/dataset/:namespace/:datasetName/version" element={<DatasetVersionListingPage/>}/>

                    <Route path="/dataset/:namespace/:datasetName/version/:version"
                           element={<DatasetMetaByVersionPage/>}/>
                    <Route path="/dataset/:namespace/:datasetName/version/:version/collection/:collName"
                           element={<DatasetSampleByVersionPage/>}/>

                </Route>

            </Route>
        </Routes>
    </BrowserRouter>
}
