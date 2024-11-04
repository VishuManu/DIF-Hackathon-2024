import { Add } from "@mui/icons-material";
import { Box, Button, DialogContent, FormControl, FormLabel, Input, Modal, ModalClose, ModalDialog, Option, Radio, RadioGroup, Select } from "@mui/joy";
import { DialogTitle, Fab } from "@mui/material";
import React, { useState } from "react";
import { ModalOverflow } from '@mui/joy';
import { Link } from "react-router-dom";


export default function GOVID() {

    const [open, set_open] = useState(false)


    return (
        <div className="w-screen h-screen" >
            <div className="w-full h-fit border-b bg-white px-8 flex flex-row justify-between py-5 px-[15%]" >
                <img className="h-16 w-16" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Seal_of_the_President_of_the_United_States.svg/220px-Seal_of_the_President_of_the_United_States.svg.png"></img>
                <p className="bg-zinc-800 h-fit w-fit border-2 border-zinc-00 text-white rounded-full px-4 py-0.5 font-bold mt-4" >did:cheqd:testnet:ad618db1-cfe9-4403-90d5-f59063ff200d</p>
            </div>
            <div className="py-12 px-[15%]">
                <div className="flex cursor-pointer  flex-col justify-between w-full">
                    <div>
                        <p className="font-bold text-5xl decoration-zinc-200 font-mono" >Goverment Ids</p>
                    </div>

                    <Link className="mt-8" to='/new_id'>
                    <Fab className="hover:bg-[#3b82f6]" color="primary" sx={{ width: 'fit-content', color: 'white', fontWeight: 'bold' }} variant="extended" >
                        <Add sx={{ mr: 1 }} />
                        New Goverment ID
                    </Fab>
                    </Link>

                </div>


            </div>
        </div>
    )
}