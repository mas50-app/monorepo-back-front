import React, {useState} from "react";

export const OutlinedInput = ({register, errors, field, watch}) => {
    const [isFocused, setIsFocused] = useState(false);

    const handleFocus = () => setIsFocused(true);
    const handleBlur = () => setIsFocused(false);

    return (
        <div className="relative">
            {field.type === 'option' && !watch(field.field)? "":
                <label
                    htmlFor={field.field}
                    style={{
                        position: "absolute",
                        top: isFocused || watch(field.field) ? "-1rem" : "50%",
                        // left: "1rem",
                        transform: isFocused || watch(field.field) ? "translateY(0)" : "translateY(-50%)",
                        transition: "all 0.2s ease-out",
                        transformOrigin: "left top",
                        fontSize: isFocused || watch(field.field) ? "0.75rem" : "1rem",
                        color: isFocused || watch(field.field) ? "#333" : "#999",
                    }}
                >
                    {field.label}
                </label>
            }

            {field.type === "option" ?
                <select
                    id={field.field}
                    {...register(field.field, {
                        required: field.required
                    })}
                    style={{
                        color: isFocused || watch(field.field) ? "#333" : "#999",
                    }}
                    className={`border-b border-gray-400 py-2 focus:outline-none focus:border-red-200 w-full ${
                        errors[field.field] ? "border-b-red-500" : "border-b-gray-200"
                    }`}
                    // className={`border-b border-gray-400 py-2 focus:outline-none ${
                    //     errors[field.field] ? "border-b-red-500" : "border-b-gray-200"
                    // } w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
                    //     !watch(field.field) && "opacity-50"
                    // }`}
                    onFocus={handleFocus}
                    onBlur={handleBlur}
                >

                    {field.options? (
                        <>
                            <option
                                value=""
                                className={`${
                                    isFocused || watch(field.field) ? "floating" : ""
                                } text-gray-400`}
                            >
                                Seleccione {field.label}
                            </option>
                            {field.options && (
                                <>
                                    <option value="" disabled hidden>
                                        {field.label}
                                    </option>
                                    {field.options.map((option, index) => (
                                        <option key={index} value={option.field}>
                                            {option.label}
                                        </option>
                                    ))}
                                </>
                            )}
                        </>
                    ): ""}

                </select>
                :
                field.type === "textarea" ?
                    <textarea
                        id={field.field}
                        {...register(field.field, {
                            required: field.required,
                        })}
                        className={`border-b border-gray-400 py-2 focus:outline-none focus:border-blue-500 w-full ${
                            errors[field.field] ? "border-b-red-500" : "border-b-gray-200"
                        }`}
                        onFocus={handleFocus}
                        onBlur={handleBlur}
                    />
                :
                    <input
                        id={field.field}
                        type={field.type}
                        {...register(field.field, {
                            required: field.required,
                        })}
                        step={field.float === true ? '0.01':'1'}
                        className={`border-b border-gray-400 py-2 focus:outline-none focus:border-red-200 w-full ${
                            errors[field.field] ? "border-b-red-500" : "border-b-gray-200"
                        }`}
                        onFocus={handleFocus}
                        onBlur={handleBlur}
                    />
            }
        </div>
    )
}



export const OutlinedSimpleInput = ({register, errors, field, watch, changeFunc}) => {
    const handleChange = (e) => {
        console.log("Cambiando", e.target.value, register[field.field])
        changeFunc(e.target.value)
        register[field.field] = e.target.value
    }
    return (
        <>
            {field.type === "option" ?
                <select
                    {...register(field.field, {
                        required: field.required
                    })}
                    className={`focus:outline-none ${
                        errors[field.field] ? "bg-red-200" : "border-b-gray-200"
                    } w-full px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
                        !watch(field.field) && "opacity-50"
                    }`}
                    onChange={handleChange}
                >

                    {field.options? (
                        <>
                            <option
                                className="text-gray-500 opacity-25"
                                key={0}
                            >
                                {`Selecciona`}
                            </option>
                            {field.options.map((optionsItem, optionsIndex) => (
                                <option
                                    className="focus:outline-none focus:ring focus:ring-red-400 hover:bg-red-400 active:bg-red-400"
                                    key={optionsIndex+1}
                                    value={optionsItem.field}
                                >
                                    {optionsItem.label}
                                </option>
                            ))}
                        </>
                    ): ""}

                </select>
                :
                field.type === "textarea" ?
                    <textarea
                        {...register(field.field, {
                            required: field.required,
                        })}
                        className={`border-b border-gray-400 focus:outline-none ${
                            errors[field.field] ? "border-b-red-500" : "border-b-gray-200"
                        } w-full px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline`}
                        onChange={handleChange}
                    />
                    :
                    <input
                        type={field.type}
                        {...register(field.field, {
                            required: field.required,
                        })}
                        step={field.type === "number" ? '0.01':'1'}
                        className={`focus:outline-none ${
                            errors[field.field] ? "border-b-red-500" : ""
                        } w-full px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline`}
                        onChange={handleChange}
                    />
            }
        </>
    )
}
