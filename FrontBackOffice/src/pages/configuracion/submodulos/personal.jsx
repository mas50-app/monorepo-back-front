import {useMutation} from "@tanstack/react-query";
import {createPersonal, deletePersonal, getPersonal, getTiposPersonal, updatePersonal} from "../../../apis/calls.js";
import React, {forwardRef, useEffect, useRef, useState} from "react";
import {Table} from "../../../components/Table.jsx";
import BasicGrill from "../../../components/BasicGrill.jsx";
import {successMessagePopUp} from "../../../components/alerts.jsx";

const IndeterminateCheckbox = forwardRef(({ indeterminate, ...rest }, ref) => {
    const defaultRef = useRef();
    const resolvedRef = ref || defaultRef;

    useEffect(() => {
        resolvedRef.current.indeterminate = indeterminate;
    }, [resolvedRef, indeterminate]);
    return (
        <>
            <input type="checkbox" ref={resolvedRef} {...rest} />
        </>
    );
});

export const Personal = () => {
    const [personal, setPersonal] = useState(null);
    const [tiposPersonal, setTiposPersonal] = useState(null);
    const [selectedRows, setSelectedRows] = useState([]);

    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        getDataTiposPersonal.mutate()
        getDataPersonal.mutate()
    }, [refresh]);


    const getDataPersonal = useMutation({
        mutationFn: getPersonal,
        onSuccess: (result) => {
            setPersonal(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const getDataTiposPersonal = useMutation({
        mutationFn: getTiposPersonal,
        onSuccess: (result) => {
            setTiposPersonal(result)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const crearPersonal = useMutation({
        mutationFn: createPersonal,
        onSuccess: (result) => {
            console.log("Personal Creado", result)
            successMessagePopUp({title:"Terminado" ,message:"Registro guardado exitosamente"})
            setRefresh((e) => !e)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const actualizaPersonal = useMutation({
        mutationFn: updatePersonal,
        onSuccess: (result) => {
            console.log("Personal Actualizado", result)
            successMessagePopUp({title:"Terminado" ,message:"Registro actualizado exitosamente"})
            setRefresh((e) => !e)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const eliminaPersonal = useMutation({
        mutationFn: deletePersonal,
        onSuccess: (result) => {
            console.log("Personal Eliminado", result)
            successMessagePopUp({title:"Terminado" ,message:"Registro eliminado exitosamente"})
            setRefresh((e) => !e)
        },
        onError: (error) => {
            console.log("error", error);
        },
    });

    const tiposPersonalOps = []

    tiposPersonal?.forEach((tipoPersonal) => {
        tiposPersonalOps.push({
            field: tipoPersonal.cod_tipo_personal,
            label: tipoPersonal.desc_tipo_personal
        })
    })

    const fields = [
        {
            field: "cod_personal",
            label: "Cod Personal",
            required: true,
            type: "text",
            show: false,
            inTable: true
        },
        {
            field: "desc_personal",
            label: "Nombre Personal",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
        {
            field: "login_personal",
            label: "Login Personal",
            required: true,
            type: "text",
            show: true,
            inTable: true
        },
        {
            field: "contrasena",
            label: "Contraseña",
            required: true,
            type: "password",
            show: true,
            inTable: false
        },
        {
            field: "cod_tipo_personal",
            label: "Tipo Personal",
            required: true,
            type: "option",
            options: tiposPersonalOps,
            show: true,
            inTable: false
        },
        {
            field: "desc_tipo_personal",
            label: "Tipo Personal",
            required: true,
            type: "text",
            show: false,
            inTable: true
        },
    ]

    return (
        <div className="flex flex-col h-full w-full m-2">
            <div className="flex flex-col justify-between p-2 mb-2 ">
                {personal &&
                    // <Table
                    //     COLUMNS={COLUMNS}
                    //     data={personal}
                    //     parentName="Personal"
                    //     hiddenColumns={[
                    //         "cod_tipo_personal"
                    //     ]}
                    //     onRowSelect={(rows) => setSelectedRows(rows)}
                    // />
                    <BasicGrill
                        tableData={personal}
                        fields={fields}
                        parentName="Personal"
                        SaveFunc={crearPersonal.mutate}
                        EditFunc={actualizaPersonal.mutate}
                        DeleteFunc={eliminaPersonal.mutate}
                    />
                }
            </div>
        </div>
    )
}