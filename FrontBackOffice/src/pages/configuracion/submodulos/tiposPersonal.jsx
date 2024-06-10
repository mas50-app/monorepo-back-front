import React, { useMemo } from 'react';
import { useState, useEffect } from 'react';
import {useMutation} from "@tanstack/react-query";
import {createTP, deleteTP, getPermisos, getTiposPersonal, updateTP} from "../../../apis/calls.js";
import BasicGrill from "../../../components/BasicGrill.jsx";
import {errorMessagePopUp, successMessagePopUp} from "../../../components/alerts.jsx";
import {FaUserShield} from "react-icons/all.js";
import {useNavigate} from "react-router-dom";

export const TiposPersonal = () => {
    const [tiposPersonal, setTiposPersonal] = useState(null);
    const [permisos, setPermisos] = useState(null);
    const [selectedTP, setSelectedTP] = useState(null);

    const [selectedPermisos, setSelectedPermisos] = useState(null);

    // const [change, setChange] = useState(false);
    const [refresh, setRefresh] = useState(false);

    const navigate = useNavigate()

    useEffect(() => {
        getDataTiposPersonal.mutate()
        getDataPermisos.mutate()
    }, [refresh]);

    // useEffect(() => {
    // }, [change]);


    const getDataTiposPersonal = useMutation({
        mutationFn: getTiposPersonal,
        onSuccess: (result) => {
            console.log("TP", result)
            setTiposPersonal(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const getDataPermisos = useMutation({
        mutationFn: getPermisos,
        onSuccess: (result) => {
            console.log("Permisos", result)
            setPermisos(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const createTipoP = useMutation({
        mutationFn: createTP,
        onSuccess: (result) => {
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo crear el registro"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Registro creado exitosamente"})
            setRefresh((e) => !e);
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const updateTipoP = useMutation({
        mutationFn: updateTP,
        onSuccess: (result) => {
            setRefresh((e) => !e);
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo actualizar el registro"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Registro actualizado exitosamente"})
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const updateTipoPPermisos = useMutation({
        mutationFn: updateTP,
        onSuccess: (result) => {
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo guardar los permisos"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Permisos actualizados exitosamente"})
            navigate("/configuracion/personal");
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const deleteTipoP = useMutation({
        mutationFn: deleteTP,
        onSuccess: (result) => {
            setRefresh((e) => !e);
            console.log(result)
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo eliminar el registro"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Registro eliminado exitosamente"})
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const fieldsTP = [
        {
            field: "cod_tipo_personal",
            label: "Cod Tipo Personal",
            required: true,
            type: "text",
            show: false,
            inTable: true
        },
        {
            field: "desc_tipo_personal",
            label: "Tipo Personal",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
        {
            field: "permisos.length",
            label: "Permisos",
            required: true,
            type: "text",
            show: false,
            inTable: false
        },
    ]

    const buttonPermisos = {
        title: "Permisos",
        funcion: (row) => {
            let cod_tipo_personal = row.values.cod_tipo_personal;
            let desc_tipo_personal = row.values.desc_tipo_personal;
            setSelectedTP(
                {
                    cod_tipo_personal: cod_tipo_personal,
                    desc_tipo_personal: desc_tipo_personal
                });
            let permisos = tiposPersonal.filter((tsp) => tsp.cod_tipo_personal === cod_tipo_personal)[0].permisos
            setSelectedPermisos(permisos)
        },
        icon: <FaUserShield/>
    }


    const handlePermisoChange = (e) => {
        const permiso = e.target.value;
        const isChecked = e.target.checked;
        if (isChecked) {
            const selNow = permisos.filter((perm) => perm.cod_permiso == permiso)
            let selected = [...selectedPermisos, selNow[0]]
            setSelectedPermisos(selected);
        } else {
            let selected = selectedPermisos.filter((perm) => perm.cod_permiso != permiso)
            setSelectedPermisos(selected);
        }
        //setChange(e=>!e)
    };

    return (
        <div className="flex flex-row h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
            <div className={`flex flex-row ${selectedTP? "w-3/4": "w-full"} h-full`}>
                {tiposPersonal &&
                    <div className="mt-4 w-full h-full border-r-2">
                        <label className="p-4">Tipos de Personal: {tiposPersonal?.length}</label>
                        <BasicGrill
                            fields={fieldsTP}
                            tableData={tiposPersonal}
                            parentName="Tipos Personal"
                            SaveFunc={createTipoP.mutate}
                            EditFunc={updateTipoP.mutate}
                            DeleteFunc={deleteTipoP.mutate}
                            buttonsField={[buttonPermisos]}
                        />
                    </div>
                }
            </div>

            {selectedTP &&
                <div className="flex flex-col w-1/4 items-center mt-8 p-4">
                    <h3
                        className="font-bold border-b border-red-400 w-full text-center mb-6 p-4"
                    >
                        Permisos de {selectedTP.desc_tipo_personal}
                    </h3>
                    <div className="flex flex-col max-w-20 mt-4">
                        {permisos.map((permiso) => (
                            <div key={permiso.cod_permiso} className="flex items-center">
                                <input
                                    type="checkbox"
                                    id={permiso.cod_permiso}
                                    name={permiso.cod_permiso}
                                    value={permiso.cod_permiso}
                                    checked={selectedPermisos.filter((sel) => sel.cod_permiso == permiso.cod_permiso).length != 0 ? true : false}
                                    onChange={handlePermisoChange}
                                    className="mr-3"
                                />
                                <label htmlFor={permiso.cod_permiso}>{permiso.desc_permiso}</label>
                            </div>
                        ))}
                        <div className="flex flex-row gap-2">
                            <button
                                onClick={() => {
                                    console.log("AAAA", selectedPermisos);
                                    updateTipoPPermisos.mutate({
                                        cod_tipo_personal: selectedTP.cod_tipo_personal,
                                        desc_tipo_personal: selectedTP.desc_tipo_personal,
                                        permisos: selectedPermisos
                                    })
                                    setSelectedTP(null)
                                }}
                                className="w-1/2 inline-block mt-4 px-7 py-3 bg-red-600  text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-red-900 hover:shadow-lg focus:bg-red-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-red-800 active:shadow-lg transition duration-150 ease-in-out"
                                data-mdb-ripple="true"
                                data-mdb-ripple-color="light"
                            >
                                Guardar
                            </button>
                            <button
                                onClick={()=>setSelectedTP(null)}
                                className="w-1/2 inline-block mt-4 px-7 py-3 bg-red-600  text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-red-900 hover:shadow-lg focus:bg-red-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-red-800 active:shadow-lg transition duration-150 ease-in-out"
                                data-mdb-ripple="true"
                                data-mdb-ripple-color="light"
                            >
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            }


        </div>
    );
};

