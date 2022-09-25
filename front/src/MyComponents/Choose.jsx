import MKButton from "components/MKButton";
import Box from "@mui/material/Box";
import MKTypography from "../components/MKTypography";
import {CssBaseline, Fade} from "@mui/material";
import React, {useEffect, useRef, useState} from 'react';
import {Link} from "react-router-dom";
import theme from "../assets/theme";
import {ThemeProvider} from "@emotion/react";


const Choose = (props) => {
    const [checked, setChecked] = useState(true);
    const tg = useRef(window.Telegram.WebApp)
    useEffect(() => {
        tg.current.BackButton.hide()
    })
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Fade timeout={1000} in={checked}>
            <Box
                sx={{
                    position: 'absolute',
                    display: 'flex',
                    justifyContent: 'center',
                    width: "100%",
                    top: "30%"
                }}
            >
                <MKTypography
                    variant="subtitle1"
                    color="dark"
                    textGradient
                >Сделай выбор</MKTypography>
            </Box>
            </Fade>
        <Fade timeout={1000} in={checked}>
            <Box sx={{

            position: 'absolute',
            display: 'flex',
            justifyContent: 'center',
            // flexDirection: 'column',
            width: '80%',
            height: '100%',
            alignItems:'center',
            left: '10%',
            // top: '50%',
            gap: '10px',

        }}>
            <Link to={'/partner'}>
                <MKButton
                    sx={{
                        overflow: "hidden"
                    }}
                    onClick={() => {setChecked(false)}}
                    variant="gradient"
                    color="warning"
                    // size='large'
                >
                    <span style={{fontSize: 23, marginRight: 18}} role="img">🚴</span>Привезти
                </MKButton>
            </Link>
            <Link to={'/customer'}>
                <MKButton
                    sx={{
                        overflow: "hidden"
                    }}
                    onClick={() => {setChecked(false)}}
                    variant="gradient"
                    color="info"
                    // size='large'
                >
                    <span
                        style={{fontSize: 23,  marginRight: 18}}
                        role="img"
                    >
                        📦
                    </span>
                    Заказать
                </MKButton>
            </Link>
        </Box>
        </Fade>
        </ThemeProvider>
    )
}
export default Choose;