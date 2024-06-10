import React, { useMemo } from 'react';
import { useState, useEffect } from 'react';
import {useMutation} from "@tanstack/react-query";
import {createBanco, deleteBanco, getBancos, updateBanco} from "../../../apis/calls.js";
import BasicGrill from "../../../components/BasicGrill.jsx";
import {errorMessagePopUp, successMessagePopUp} from "../../../components/alerts.jsx";
import {FaUserShield} from "react-icons/all.js";

export const Bancos = () => {
    const [bancos, setBancos] = useState(null);

    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        getDataBancos.mutate()
    }, [refresh]);

    // useEffect(() => {
    // }, [change]);


    const getDataBancos = useMutation({
        mutationFn: getBancos,
        onSuccess: (result) => {
            setBancos(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const crearBanco = useMutation({
        mutationFn: createBanco,
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

    const actualizarBanco = useMutation({
        mutationFn: updateBanco,
        onSuccess: (result) => {
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo actualizar el registro"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Registro actualizado exitosamente"})
            setRefresh((e) => !e);
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const eliminarBanco = useMutation({
        mutationFn: deleteBanco,
        onSuccess: (result) => {
            if (result === null) {
                errorMessagePopUp({title: "Error", message: "No se pudo eliminar el registro"})
                return
            }
            successMessagePopUp({title:"Terminado", message:"Registro eliminado exitosamente"})
            setRefresh((e) => !e);
        },
        onError: (error) => {
            console.log("error", error);
        },
    });


    const fieldsTP = [
        {
            field: "cod_banco",
            label: "Cod banco",
            required: true,
            type: "text",
            show: false,
            inTable: true
        },
        {
            field: "desc_banco",
            label: "Banco",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
    ]

    return (
        <div className="flex flex-row h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
            <div className={`flex flex-row w-full h-full`}>
                {bancos &&
                    <div className="mt-4 w-full h-full border-r-2">
                        <label className="p-4">Bancos: {bancos?.length}</label>
                        <BasicGrill
                            fields={fieldsTP}
                            tableData={bancos}
                            parentName="Bancos"
                            SaveFunc={crearBanco.mutate}
                            EditFunc={actualizarBanco.mutate}
                            DeleteFunc={eliminarBanco.mutate}
                        />
                    </div>
                }
            </div>
        </div>
    );
};

