import React from 'react';
import './App.css';
import {AppRoutes} from "./routes";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {HelmetProvider} from 'react-helmet-async';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false, // default: true
            retry: 1
        },
    },
})


function App() {
    return (
        <HelmetProvider>
            <QueryClientProvider client={queryClient}>
                <AppRoutes/>
            </QueryClientProvider>
        </HelmetProvider>
    );
}

export default App;
