import React from 'react';
import ReactDOM from 'react-dom';

const test = <p>hello word!</p>

const root = document.createElement('div');
document.body.appendChild(root)
ReactDOM.render(test, root)