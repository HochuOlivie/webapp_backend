import React, {useEffect, useRef, useState} from 'react';
import TextField from "@mui/material/TextField";
import SearchIcon from '@mui/icons-material/Search';
import {InputAdornment} from "@mui/material";
import IconButton from '@mui/material/IconButton';
import fetchJsonp from "fetch-jsonp";
import {blue, grey} from '@mui/material/colors';

const Search = (props) => {
    let map = props.map
    let ymaps = props.ymaps
    let objectManager = props.objectManager
    let setCurrentFeatures = props.setCurrentFeatures

    let [text, setText] = useState('')

    const drawerText= props.drawerText
    const setDrawerText= props.setDrawerText

    const searchInput = useRef(null);

    const handleTextFieldChange = (e) => {
        setText(e.target.value)
    }

    const keyDown = (e) => {
        if (e.keyCode === 13) {
            searchInput.current.blur()
            performSearch(text)
        }
    }

    const placeFeatureCollection = (data) => {
        console.log(data)
        // objectManager.removeAll()
        data.features = data.features.map((element, id) => {
            element.id = id
            element.geometry.coordinates.reverse()
            return element
        })
        setCurrentFeatures(data)
        // objectManager.add(data);
        map.setBounds(objectManager.getBounds(), {
            checkZoomRange: true,
        })
    }

    const performSearch = (text) => {
        // placeFeatureCollection({})
        fetchJsonp(`https://search-maps.yandex.ru/v1/?text=${text},Новосибирск&type=biz&lang=ru_RU&apikey=3eeb727a-9b93-4fde-80c2-07b68a6073d5&results=500`, {
            jsonpCallback: "callback"
        })
            .then((res) => res.json())
            .then((data) => placeFeatureCollection(data))
            .catch(function(ex) {
            console.log('parsing failed', ex)
        })
    }

    return (
            <TextField
                size="small"
                ref={searchInput}
                sx={{
                    // boxShadow: 3,
                    // borderRadius: '10px 10px 0 0',
                    position: 'absolute',
                    top: '10px',
                    width: '90%',
                    left: '5%',
                    right: '5%',
                    '& .MuiOutlinedInput-root': {
                        backgroundColor: 'white',
                        background: 'white',
                        boxShadow: 1,
                        '& fieldset': {
                            borderColor: 'white',
                        },
                        '&:hover fieldset': {
                            borderColor: 'white',
                        },
                        '&.Mui-focused fieldset': {
                            borderColor: 'white',
                        },
                        // borderRadius: '10px 10px 0 0',
                    },
                    '& .MuiOutlinedInput-root.Mui-focused': {
                        backgroundColor: 'white',
                        background: 'white',
                    },
                    '& .MuiOutlinedInput-root:hover': {
                        backgroundColor: 'white',
                        background: 'white',
                    },
                    '& label.Mui-focused': {
                        color: 'white',
                    },
                    '& .MuiInput-underline:after': {
                        borderBottomColor: 'white',
                    },
                }}
                InputProps={{
                    startAdornment: <InputAdornment position='start'>
                        <SearchIcon sx={{position: 'relative', right: '5px'}} color={'primary'}/>
                    </InputAdornment>,
                }}

                onKeyDown={keyDown}
                onChange={handleTextFieldChange}
                // label='Поиск'
                // defaultValue="Поиск"
                variant="outlined"
            />
    )
}

export default Search;