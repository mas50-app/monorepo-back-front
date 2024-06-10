import {useEffect, useRef, useState} from "react";
import { useForm } from "react-hook-form";
import { questionMessagePopUp } from "./alerts";
import ChileanRutify from "chilean-rutify";
import { Table } from "./Table";
import { RiDeleteBin7Line, RiEdit2Line } from "react-icons/ri";
import {OutlinedInput} from "./forms/Inputs.jsx";

export default function BasicGrill({fields, NewFunc, SaveFunc, EditFunc, DeleteFunc, tableData, buttons, buttonsField, parentName}) {

  const { register, handleSubmit, setValue , formState: { errors, isSubmitSuccessful }, watch, reset } = useForm()

  const [isEditing, setIsEditing] = useState(false)

  const formRef = useRef()

    useEffect(() => {
        if (isSubmitSuccessful){
            reset()
        }
    }, [isSubmitSuccessful]);


  // Aqui se arman las columnas que utilizará la tabla según los fields pasados
  const COLUMNS = []
  const hiddenColumns = []

  fields.forEach(elem => {
      if (elem.inTable === false) {
          hiddenColumns.push(elem.field)
      }
      COLUMNS.push(
          elem.Cell?
          {
              Header: elem.label,
              accessor: elem.field,
              Cell: elem.Cell
          }:
              {
                  Header: elem.label,
                  accessor: elem.field
              }
      )
  })
  COLUMNS.push(
    {
        width : 300,
        Header: ' ',
        Cell: ({row}) => (
            <div className="btn-group justify-end text-right">
                {buttonsField?.map((boton, key) =>
                    // boton.showButton(row) &&
                        <button
                            key={key}
                            title={boton.title}
                            type="button"
                            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            onClick={() => boton.funcion(row)}
                        >{boton.icon}
                        </button>

                )}
                <button
                    title="Editar"
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    onClick={() => HandleEdit(row.values)}><RiEdit2Line/></button>
                <button
                    title="Eliminar"
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    onClick={() => HandleDelete(row.values)}><RiDeleteBin7Line/>
                </button>
           </div>
        )
    }
  )
  //-----------------------------------------------------------------------------

  const HandleNuevo = (e) => {
    e.preventDefault()
      if (NewFunc){
          NewFunc()
      }else{
          const resetForm =  () => {
              reset()
              setIsEditing(false)
          }
          questionMessagePopUp({title:"Está seguro que desea perder los campos ingresados?", functionOnConfirm:resetForm})
      }

} 

  const HandleGuardar = (data) => { 
    if (isEditing === false){
        SaveFunc(data)
    }else{
        EditFunc(data)
        setIsEditing(false)
    }

    // formRef.current?.reset()
}

const HandleEdit = (item) => {
    if (EditFunc === undefined) {
        return
    }
    const Edit = () => {
        Object.keys(item).forEach(key => {
            setValue(key, item[key])
            setIsEditing(true)
        });
        formRef.current[formRef.current.length-1].focus()
      }
    questionMessagePopUp({title:"Desea editar este registro?", functionOnConfirm:Edit})
     
  }


const HandleDelete = (item) => {
    if (DeleteFunc === undefined) {
        return
    }
    
    const Del = () => {
        let aEliminar = {
             
        }
        aEliminar[fields[0].field] = item[fields[0].field]
        DeleteFunc(aEliminar)
    }
    questionMessagePopUp({title:"Desea eliminar este registro?", functionOnConfirm:Del})
}

  const HandleRutChange = (e) => {
    console.log(ChileanRutify.formatRut(e.target.value))
    setValue(e.target.name, ChileanRutify.formatRut(e.target.value)) 
}

  return (
        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        <>
        <form
            onSubmit={handleSubmit(HandleGuardar)}
            ref={formRef}
            className="p-4 pr-6 border-1-8 border-transparent rounded-md shadow-md space-y-2"
        >
            {/* Botonera */}
            <button
                    onClick={HandleNuevo}
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                > Nuevo
            </button>
            <button
                    type="submit"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    > Guardar
            </button>
            {/* Botones Extras */}
            {buttons?(
                
                buttons.map((elem, index) => (
                    <button
                    onClick={elem.func? elem.func: ()=> console.log(`No se le asoció función al botón ${elem.name}`)}
                    key={index}
                    type="button"
                    className="inline-flex rounded justify-center border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        > {elem.name}
                    </button>
                    
                ))
                
                ): ("")}
            
            {/* Fin de la Botonera */}
            <hr/>
            <div className="flex flex-wrap p-2">
            {fields ? (
                    fields.slice(1).map((item, index) => (
                            item.show ? (
                                <div key={index} className="flex w-1/1 p-2">
                                    <OutlinedInput
                                        register={register}
                                        errors={errors}
                                        watch={watch}
                                        field={item}
                                    />
                                </div>
                            ): ("")
                    ))
            ):(
                ""
            )}
            </div>            
        </form>
        <br/>
        <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
            {tableData? (<Table COLUMNS={COLUMNS} parentName={parentName} data={tableData} hiddenColumns={hiddenColumns}/>):""}
        </div>
        </>
  );
}