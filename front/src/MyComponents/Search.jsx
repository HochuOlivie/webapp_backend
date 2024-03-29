import React, {useRef, useState} from 'react';
import TextField from "@mui/material/TextField";
import SearchIcon from '@mui/icons-material/Search';
import {InputAdornment} from "@mui/material";
import fetchJsonp from "fetch-jsonp";

const Search = (props) => {
    let map = props.map
    let objectManager = props.objectManager
    let setCurrentFeatures = props.setCurrentFeatures
    let city = props.city
    let [text, setText] = useState('')

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
        data.features = data.features.map((element, id) => {
            element.id = id * 2 + 1
            element.geometry.coordinates.reverse()
            return element
        })
        data.features = data.features.filter(function(item) {
            return item.properties.description.includes(city.current)
        });

        setCurrentFeatures(data.features)
        map.setBounds(objectManager.getBounds(), {
            checkZoomRange: true,
        })
    }

    const performSearch = (text) => {
        // placeFeatureCollection({})
        fetchJsonp(`https://search-maps.yandex.ru/v1/?text=${text},${city.current}&type=biz&lang=ru_RU&apikey=3eeb727a-9b93-4fde-80c2-07b68a6073d5&results=500`, {
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