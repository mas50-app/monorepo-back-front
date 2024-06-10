import React, {useState, useEffect} from "react";
import { useForm } from "react-hook-form";
import {OutlinedInput} from "../../components/forms/Inputs.jsx";
import {useMutation} from "@tanstack/react-query";
import {getAppData, updateAppData} from "../../apis/calls.js";


export const AppM = () => {
    const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm();
    const [data, setData] = useState(false);
    const [refresh, setRefresh] = useState(false);

    const onSubmit = (data) => {
        console.log(data);
        updateApplicationData.mutate(data)
    };

    useEffect(() => {
        getApplicationData.mutate()
    }, [refresh]);


    const getApplicationData = useMutation({
        mutationFn: getAppData,
        onSuccess: (result) => {
            setData(result)
            Object.keys(result).forEach(key => {
                setValue(key, result[key])
            });
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const updateApplicationData = useMutation({
        mutationFn: updateAppData,
        onSuccess: (result) => {
            setRefresh((e) => !e)

        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const fields = [
        {
            field: "cod_compra_activa",
            label: "Compra Activa",
            type: "option",
            required: true,
            options: [
                {
                    field: "S",
                    label: "S"
                },
                {
                    field: "N",
                    label: "N"
                }
            ]
        },
        {
            field: "cod_venta_activa",
            label: "Venta Activa",
            type: "option",
            required: true,
            options: [
                {
                    field: "S",
                    label: "S"
                },
                {
                    field: "N",
                    label: "N"
                }
            ]
        },
        {
            field: "comision_mas_50_default",
            label: "Comisión General",
            type: "number",
            float: true,
            required: true
        },
        {
            field: "terminos_condiciones_url",
            label: "Términos y Condiciones",
            type: "text",
            required: true
        },
        {
            field: "politicas_privacidad_url",
            label: "Políticas de Privacidad",
            type: "text",
            required: true
        },
    ]

    return (
        <div className="flex flex-col h-full w-full justify-center items-center text-center bg-white shadow-lg rounded-sm border border-gray-200 m-2">
            <label
                className="mt-6 uppercase text-xl text-gray-700 font-bold mb-4 p-4 rounded-lg border border-red-900 bg-red-200"
            >
                Configuración General de la App
            </label>
            <label className="mt-3 text-gray-400 mb-4">Versión {data?.version}</label>
            <div className="flex flex-col h-full w-full justify-center items-center">
                <div className="flex flex-col w-1/2 h-full border border-red-200 rounded-lg justify-center items-center p-5 mb-5 shadow-lg">
                    <label className="p-4 m-10 h-1/3">Estado Global</label>
                    <form onSubmit={handleSubmit(onSubmit)} className="w-full h-2/3 max-w-lg mx-auto">
                        <div className="flex flex-wrap -mx-3 mb-6">
                            <div className="flex flex-col w-full gap-6">
                                {fields.map((field, index) => (
                                    <OutlinedInput
                                        key={index}
                                        register={register}
                                        watch={watch}
                                        errors={errors}
                                        field={field}
                                    />
                                ))}
                            </div>
                        </div>
                        <button
                            type="submit"
                            className="inline-block mt-4 px-7 py-3 bg-red-600  text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-red-900 hover:shadow-lg focus:bg-red-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-red-800 active:shadow-lg transition duration-150 ease-in-out"
                            data-mdb-ripple="true"
                            data-mdb-ripple-color="light"
                        >
                            Guardar Cambios
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}