import BasicGrill from "../../components/BasicGrill.jsx";
import React, {useEffect, useState} from "react";
import {useMutation} from "@tanstack/react-query";
import {createBanco, createCourier, deleteCourier, getCouriers, updateCourier} from "../../apis/calls.js";
import {errorMessagePopUp, successMessagePopUp} from "../../components/alerts.jsx";


const IMAGE_SERVER_API = import.meta.env.VITE_IMAGES_API;

export const mantenedorCourier = () => {

    const [couriers, setCouriers] = useState(null);
    const [refresh, setRefresh] = useState(null);

    useEffect(() => {
        getDataCouriers.mutate()
    }, [refresh]);



    const getDataCouriers = useMutation({
        mutationFn: getCouriers,
        onSuccess: (result) => {
            setCouriers(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });


    const crearCourier = useMutation({
        mutationFn: createCourier,
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

    const actualizarCourier = useMutation({
        mutationFn: updateCourier,
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

    const eliminarCourier = useMutation({
        mutationFn: deleteCourier,
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

    const handleCrear = (data) => {
        const cuerpo = {
            img: data.img ? data.img[0] : null ,
            desc_courier: data.desc_courier,
            link_courier: data.link_courier
        }
        crearCourier.mutate(cuerpo)
    }

    const handleActualizar = (data) => {
        console.log("antes de armar", data)
        const cuerpo = {
            img: data.img ? data.img[0] : null ,
            cod_courier: data.cod_courier,
            desc_courier: data.desc_courier,
            link_courier: data.link_courier
        }
        actualizarCourier.mutate(cuerpo)
    }


    const fields = [
        {
            field: "cod_courier",
            label: "Cod Courier",
            required: true,
            type: "number",
            show: false,
            inTable: true
        },
        {
            field: "desc_courier",
            label: "Courier",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
        {
            field: "link_courier",
            label: "Link Courier",
            required: true,
            type: "text",
            show: true,
            inTable: true,
            Cell: ({row}) => (
                <a
                    className="hover:text-blue-400 transition-1.2"
                    href={row.values.link_courier}
                >
                    {row.values.link_courier}
                </a>
            )
        },
        {
            field: "path_imagen",
            label: "Path Imagen",
            required: false,
            type: "text",
            show: false,
            inTable: false
        },
        {
            field: "img",
            label: "Logo",
            required: false,
            type: "file",
            show: true,
            inTable: true,
            Cell: ({row}) => (
                <div className="flex justify-center items-center">
                    {row.values.path_imagen ?
                        <img
                            src={`${IMAGE_SERVER_API}${row.values.path_imagen}`}
                            alt="Logo Courier"
                            className="w-12 h-12 rounded rounded-md"
                        />:
                        <p>N/T</p>
                    }
                </div>
            )
        },
    ]
    return (
        <div className={`flex flex-row w-full h-full`}>
            {couriers &&
                <div className="mt-4 w-full h-full">
                    <label className="p-4">Couriers: {couriers?.length}</label>
                    <BasicGrill
                        fields={fields}
                        tableData={couriers}
                        parentName="Couriers"
                        SaveFunc={handleCrear}
                        EditFunc={handleActualizar}
                        DeleteFunc={eliminarCourier.mutate}
                    />
                </div>
            }
        </div>
    )
}