import React, { useMemo } from 'react';
import { useState, useEffect } from 'react';
import {useMutation} from "@tanstack/react-query";
import {
    createTiposCuentaBancaria, deleteTiposCuentaBancaria,
    getBancos,
    getTiposCuentaBancaria,
    updateTiposCuentaBancaria
} from "../../../apis/calls.js";
import BasicGrill from "../../../components/BasicGrill.jsx";
import {errorMessagePopUp, successMessagePopUp} from "../../../components/alerts.jsx";
import {FaUserShield} from "react-icons/all.js";

export const TiposCuentaB = () => {
    const [tiposCB, setTiposCB] = useState(null);

    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        getDataTiposCB.mutate()
    }, [refresh]);

    // useEffect(() => {
    // }, [change]);


    const getDataTiposCB = useMutation({
        mutationFn: getTiposCuentaBancaria,
        onSuccess: (result) => {
            setTiposCB(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const crearTipoCuentaB = useMutation({
        mutationFn: createTiposCuentaBancaria,
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

    const actualizarTipoCuentaB = useMutation({
        mutationFn: updateTiposCuentaBancaria,
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

    const eliminarTipoCuentaB = useMutation({
        mutationFn: deleteTiposCuentaBancaria,
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
            field: "cod_tipo_cuenta_bancaria",
            label: "Cod Tipo Cuenta Bancaria",
            required: true,
            type: "text",
            show: false,
            inTable: true
        },
        {
            field: "desc_tipo_cuenta_bancaria",
            label: "Tipo Cuenta Bancaria",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
    ]

    return (
        <div className="flex flex-row h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
            <div className={`flex flex-row w-full h-full`}>
                {tiposCB &&
                    <div className="mt-4 w-full h-full border-r-2">
                        <label className="p-4">Tipos Cuenta Bancaria: {tiposCB?.length}</label>
                        <BasicGrill
                            fields={fieldsTP}
                            tableData={tiposCB}
                            parentName="Tipos Cuenta Bancaria"
                            SaveFunc={crearTipoCuentaB.mutate}
                            EditFunc={actualizarTipoCuentaB.mutate}
                            DeleteFunc={eliminarTipoCuentaB.mutate}
                        />
                    </div>
                }
            </div>
        </div>
    );
};

