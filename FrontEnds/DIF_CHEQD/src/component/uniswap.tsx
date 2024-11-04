import { Add, Check, CurrencyBitcoin, Fingerprint, Money } from "@mui/icons-material";
import { Box, Button, DialogContent, FormControl, FormLabel, Input, Modal, ModalClose, ModalDialog, Option, Radio, RadioGroup, Select, Step, StepButton, StepIndicator, Stepper } from "@mui/joy";
import { DialogTitle, Divider } from "@mui/material";
import React, { useEffect, useState } from "react";
import { ModalOverflow } from '@mui/joy';
import { Link } from "react-router-dom";
import axios from "axios";
import QRCode from "react-qr-code";
import { JsonView, allExpanded, darkStyles, defaultStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

export default function DEFI() {


    const port = 5001

    const [open, set_open] = useState(false)
    const [invite_url, set_invite_url] = useState("")
    const steps = ['Provide Goveremnt Id', 'Provide Biometrics', 'Saving to IPFS', 'Credential Issued'];
    const [new_connection_modal, set_new_connection_modal] = useState(false)
    const [activeStep, setActiveStep] = React.useState(0);
    const [goverm_id_ask, set_goverm_id_ask] = useState(false)
    const [peers, set_peers] = useState([])
    const [is_verofy, set_verify] = useState(false)
    const [to_show, set_to_show] = useState({})
    const [asked_peer, set_asked_peer] = useState<string>("");
    const [is_loading, set_loading] = useState(false)
    async function send_inviate() {
        set_new_connection_modal(true)

        const _create_invite = await axios.get(`http://localhost:5000/connections/create-invitation/defi`)
        console.log(_create_invite)
        if (_create_invite.status == 200) {
            set_invite_url(_create_invite.data)
            set_new_connection_modal(true)
        }
    }



    useEffect(() => {
        async function get() {
            const data = await axios.get("http://localhost:5005/get_data/defi")
            if (data.status == 200) {
                set_peers(JSON.parse(data.data.replace(/'/g, '"')))
            }
        }
        get()
        console.log(peers)
    }, []);

    return (
        <div className="w-screen h-screen bg-black" >
            <div className="w-full h-fit px-8 flex flex-row justify-between py-5 px-[15%]" >
                <CurrencyBitcoin sx={{ fontSize: '48px', color: "white" }}></CurrencyBitcoin>
                <div className="flex flex-row gap-4">
                    <div className="flex flex-row gap-4">
                        <p onClick={() => {
                            send_inviate()
                        }} className="bg-zinc-800 h-fit w-fit text-zinc-100 text-sm rounded-full px-4 py-1 font-bold mt-4" >New DID Connection</p>


                    </div>

                </div>
            </div>
            <div>
                <center>
                    <div className="rounded-xl  max-w-[30%] h-24">
                        <p className="text-white font-bold text-white text-4xl pt-32" >Send Money To Anyone In World.</p>
                        <div className="flex flex-col justify-between w-full">
                            <div className="flex flex-row mt-16 w-full gap-4">
                                <input placeholder="$" disabled className="w-12 bg-transparent placeholder-gray-400 text-white font-bold text-7xl focus:outline-none" ></input>

                                <input placeholder="5" className="bg-transparent placeholder-gray-400 text-white font-bold text-7xl focus:outline-none" ></input>
                            </div>

                            {
                                is_verofy ? (
                                    <Button className="h-fit" sx={{ borderRadius: '100px', fontSize: '24px', px: '24px', mt: '48px' }} >Send</Button>

                                ) : (
                                    <Button onClick={() => {
                                        set_goverm_id_ask(true)
                                    }} className="h-fit" sx={{ borderRadius: '100px', fontSize: '24px', px: '24px', mt: '48px' }} >Verify</Button>

                                )
                            }
                        </div>
                    </div>
                </center>
            </div>
            <Modal open={new_connection_modal} onClose={() => set_new_connection_modal(false)}>
                <ModalOverflow>
                    <ModalDialog sx={{ width: '30%' }}>
                        <div className="max-w-xl mx-auto py-8">
                            <p className="text-xl font-semibold my-4  h-fit" >New Connection</p>
                            <QRCode
                                height={256}
                                style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                                value={invite_url}
                            />
                            <Input sx={{ mt: '16px' }} value={invite_url} disabled ></Input>

                            <Button onClick={() => {
                            }} className="w-full" sx={{ borderRadius: '100px', mt: '32px' }} variant="soft" >Copy Invite Url</Button>
                        </div>
                    </ModalDialog>
                </ModalOverflow>
            </Modal>


            <Modal open={goverm_id_ask} onClose={() => set_goverm_id_ask(false)}>
                <ModalOverflow>
                    <ModalDialog sx={{ width: '35%' }} orientation="vertical">
                        <div className="">
                            <p className="text-xl font-semibold my-4  h-fit" >Ask For credential</p>
                            <div className="grid grid-cols-1">

                                <div>
                                    <p>From</p>
                                    <Select onChange={(event: React.SyntheticEvent | null,
                                        newValue: string | null,) => {
                                        set_asked_peer(newValue)
                                    }} >
                                        {
                                            peers.map((value: any, index: number) => {
                                                return (<Option className="truncate w-[400px]" value={value['peers']['their_did']} key={value['peers']["connection_id"]} >{value['peers']['their_did']}</Option>);
                                            })
                                        }
                                    </Select>
                                </div>

                                <div className="bg-zinc-100 border border-zinc-300  mt-8 rounded-lg w-full h-fit">
                                    <JsonView data={to_show} shouldExpandNode={allExpanded} style={defaultStyles} />
                                </div>
                            </div>
                            <Button onClick={async () => {

                                if (asked_peer.trim().length > 0) {
                                    let _d = await axios.post(`http://localhost:5000/ask_presentation/defi/${asked_peer}`);
                                    set_to_show(_d.data)

                                }

                            }} className="w-full" sx={{ borderRadius: '100px', mt: '32px' }} variant="soft" >Send Credential Request</Button>
                        </div>
                    </ModalDialog>
                </ModalOverflow>
            </Modal>
        </div>
    )
}