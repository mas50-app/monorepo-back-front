import React, {useState} from "react";
import {AppM} from "./app.jsx";
import {Personal} from "./submodulos/personal.jsx";
import {TiposPersonal} from "./submodulos/tiposPersonal.jsx";


const tabs = [
    { name: 'Cuentas Personal', component: Personal },
    { name: 'Tipos Personal', component: TiposPersonal },
    // { name: 'Permisos', component: Permisos },
    // { name: 'Configuración App', component: AppM },
    // { name: 'Billing', href: '#', current: false },
]

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export function MantenedorUsuarios() {
    const [activeTab, setActiveTab] = useState("Cuentas Personal");
    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };
    return (
        <div className="flex flex-col w-full h-full">
            <ul className="flex justify-around mb-4">
                {tabs.map((tab, index) => (
                    <li
                        className={`cursor-pointer w-1/${tabs.length} py-4 px-1 text-center border-b-2 font-medium text-md ${tab.name === activeTab
                        ? 'border-red-500 text-red-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                        key={index}
                        onClick={() => handleTabClick(tab.name)}
                    >
                        {tab.name}
                    </li>
                ))}
            </ul>
            <div className="flex w-full h-full justify-center items-center">
                {tabs.map((tab, index) => (

                    activeTab === tab.name && <tab.component key={index}/>
                ))}
            </div>
        </div>

    )
}