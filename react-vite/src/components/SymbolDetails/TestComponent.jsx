// Test component for SymbolDetails for debugging purposes  

import React from 'react';

console.log("TestComponent module loaded");

class TestComponent extends React.Component {
    constructor(props) {
        super(props);
        console.log("TestComponent constructor called");
    }

    render() {
        console.log("TestComponent render called");
        return <div>Test Component</div>;
    }
}

console.log("Exporting TestComponent");
export default TestComponent; 