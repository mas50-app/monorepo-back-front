import React from "react";

export const GlobalFilter = ({filter, setFilter}) => {
    return (
        <label className="flex gap-x-2 mx-5 items-baseline">
        <span style={{justifySelf:'flex-start'}} className="text-gray-700">
            Buscar: {' '} &nbsp;
            
        </span>
        <input value={filter || ''}
            type="text"
            className="appearance-none block px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            onChange={e => setFilter(e.target.value)}
        />
        </label>
    )
}