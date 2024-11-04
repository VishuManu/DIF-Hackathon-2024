import { Add, Check, Fingerprint, FingerprintRounded } from "@mui/icons-material";
import { Box, Button, CircularProgress, DialogContent, FormControl, FormLabel, Input, LinearProgress, Modal, ModalClose, ModalDialog, Option, Radio, RadioGroup, Select, Step, StepButton, StepIndicator, Stepper, Textarea } from "@mui/joy";
import { DialogTitle } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import { ModalOverflow } from '@mui/joy';
import { Link } from "react-router-dom";
import axios from "axios";
import QRCode from "react-qr-code";
import { JsonView } from "react-json-view-lite";


export default function BIOM() {


    const port = 5001

    const [open, set_open] = useState(false)
    const [invite_url, set_invite_url] = useState("")
    const steps = ['Provide Goveremnt Id', 'Provide Biometrics', 'Creating Z-Snark Circuit', 'Credential Issued'];
    const [new_connection_modal, set_new_connection_modal] = useState(false)
    const [activeStep, setActiveStep] = React.useState(0);
    const [goverm_id_ask, set_goverm_id_ask] = useState(false)
    const inp_ref = useRef(null);
    const [data, set_data] = useState("")
    const [peers, set_peers] = useState([])
    const [is_did_doc_open, set_did_doc_open] = useState(false)
    const [did_doc, set_did_doc] = useState(null)
    const [circuit_creation, set_circuit_creation] = useState(false)
    const [asked_peer, set_asked_peer] = useState<any>("");
    const [is_loading, set_loading] = useState(false)
    async function send_inviate() {
        const _create_invite = await axios.get("http://localhost:5000/connections/create-invitation/biometrics")
        console.log(_create_invite)
        if (_create_invite.status == 200) {
            set_invite_url(_create_invite.data)
            set_new_connection_modal(true)
        }
    }
    const uploadImage = async (imageFile: any) => {
        const formData = new FormData();
        formData.append('file', imageFile);
        formData.append("to_peer", "did:peer:4zQmfVscY9Mhj2oKbk4YLLhVkhSJv9Aa765EgPt7kyvtZ5L3:z24v8eDtghRpQqS9MMzp5RPcxyNZoKZB9c9QFPXe9DU7bSZ6Co63fPPquwHHp5cPdJyBakfaS7rGeiWAHLPUe8GVBNPq4zM1hc4zXkGmVyer32Ft8fMDScmwG28xTGjhAryiXNqMCsJcHQwnmNzAhu7MUu5QS6WinVuR4pmMsKw36YcsgPdFQmEN9EvS3ouX6ANBdMauSk8WJVM44DzRDd82SumJcD68TNgnNZoXBdPWjyt875td1F2FkSgqq5RzoQwqQFH8CcZe72CRrYXXKTLtgXZjC3VoUQg5kURpMhotdy99kvAzcvGFwH8DfADGPscq4qQDt82QuVquJe78zcuM2KZKrPoLDTD7ebELHe6sK6tsHEsDtkWztrwXsftmkqLFGaCfY5NpoGKNyzMkMyZbFPs4imcrqjpoe8WUfBjdg24oiUdtBBE7zUFELPfSc8TD2p9DEsaDnTM1Cys7UBXWLWUnXFFAFzV3H9TapGKv8rYakVX9b7A2Wa739PhBPDNtLbckB98D1gTS134hJp7FsJyjpoy6GQaEZ47bNwgcWSvwh1q62v3D9cGuzDLpaN9HBAaqbX2LRy56VRXp3S81XdCAyxNdbHLYoEHhzmkWFefHMEFbTMQAAXZVHArCSDjWvzPwuS8rrcyratxHGgBiccG39S1qB1Tq5pYp8QezE3vGB4wy1k6BQ4Skj3TVEXELvCXtzadQVX8P59aPxkGq61pmuwoQ6gfHXr")
        formData.append("to_key", "did:key:zMS63derBw9PkDK3ziWaaK6hwDimyhCeLLUndr2zu5s3LEm8JPwsQG8pKNawTCT1W2pE1148Lvbc1To4b5hbhgYWJ3")
        formData.append('issuer', 'did:cheqd:testnet:e1e53efb-6472-48fb-96e3-904dc98ddc20')

        try {
            set_circuit_creation(true)
            const response = await axios.post('http://localhost:5000/create_biometric_credential', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            set_data(response.data['credential'])
            setActiveStep(3)
            set_circuit_creation(false)
            console.log(response.data);
        } catch (error) {
            console.error("There was an error uploading the image!", error);
        }
    };
    const handleImageUpload = (event: any) => {
        const imageFile = event.target.files[0];
        if (imageFile) {
            uploadImage(imageFile);
        }
    };
    useEffect(() => {
        async function get() {
            const data = await axios.get("http://localhost:5005/get_data/biometrics")
            if (data.status == 200) {
                console.log(data.data)
                set_peers(JSON.parse(data.data.replace(/'/g, '"')))
                console.log(peers)
            }
        }
        get()
    }, []);

    return (
        <div className="w-screen h-screen" >
            <div className="w-full h-fit border-b bg-white px-8 flex flex-row justify-between py-5 px-[15%]" >
                <Fingerprint sx={{ fontSize: '48px' }}></Fingerprint>
                <div className="flex flex-row gap-4">
                    <p onClick={() => {
                        send_inviate()
                    }} className="bg-zinc-100 h-fit w-fit text-zinc-800 text-sm rounded-full px-4 py-1 font-bold mt-4" >New DID Connection</p>

                    <p onClick={async () => {
                        set_did_doc_open(true)
                        fetch('https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:e1e53efb-6472-48fb-96e3-904dc98ddc20')
                            .then((res) => {
                                return res.json();
                            })
                            .then((data) => {
                                set_did_doc(data)
                            });

                    }} className=" cursor-pointer bg-zinc-800 h-fit w-fit border-2 border-zinc-00 text-white rounded-full px-4 py-0.5 font-bold mt-4" >did:cheqd:testnet:e1e53efb-6472-48fb-96e3-904dc98ddc20</p>

                </div>
            </div>
            {
                is_loading && (
                    <LinearProgress />
                )
            }
            <div className="py-12 px-[15%]">
                <div className="flex cursor-pointer  flex-row justify-between w-full">
                    <div>
                        <p className="font-bold text-4xl decoration-zinc-200 font-mono" >Biometric Credentials</p>
                    </div>



                </div>

                <Stepper orientation="vertical" sx={{ width: '100%', mt: '100px' }}>
                    {steps.map((step, index) => (
                        <Step
                            key={step}
                            indicator={
                                <StepIndicator
                                    variant={activeStep <= index ? 'soft' : 'solid'}
                                    color={activeStep < index ? 'neutral' : 'primary'}
                                >
                                    {activeStep <= index ? index + 1 : <Check />}
                                </StepIndicator>
                            }
                            sx={[
                                activeStep > index &&
                                index !== 2 && { '&::after': { bgcolor: 'primary.solidBg' } },
                            ]}
                        >
                            <StepButton onClick={() => {
                                if (index == 0) {
                                    set_goverm_id_ask(true)
                                }
                                if (index == 1) {

                                }
                            }}>{step}</StepButton>
                        </Step>
                    ))}
                </Stepper>

                {
                    activeStep == 1 && (
                        <div className="flex mt-24 flex-col">
                            <center>
                                <div className="border  border-zinc-400 border-dashed rounded-lg w-fit p-6" >
                                    <p className="font-bold mb-4 text-sm" >Provide Fingerprint Scan</p>
                                    <div className="border w-fit border-zinc-400 rounded-lg p-2 border-dashed">
                                        <FingerprintRounded sx={{ fontSize: '50px' }} ></FingerprintRounded>
                                    </div>
                                    <input ref={inp_ref} hidden type="file" name="file" accept="image/*" onChange={handleImageUpload} />

                                    <Button onClick={() => {

                                        inp_ref.current.click();
                                    }} sx={{ borderRadius: '100px', mt: '24px' }} >Attach</Button>


                                    {
                                        circuit_creation && (
                                            <center>
                                                <div className="w-fit flex gap-4 flex-col" >
                                                    <p className="text-xs mt-6 font-semibold">Z-Snark Circuit Creating</p>
                                                    <center>
                                                        <CircularProgress size="sm"></CircularProgress>

                                                    </center>
                                                </div>
                                            </center>
                                        )
                                    }
                                </div>
                            </center>
                        </div>
                    )
                }

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

                <Modal open={open} onClose={() => set_open(false)}>
                    <ModalDialog sx={{ width: '30%' }} size='lg'>
                        <ModalClose />
                        <p>Claim Biometrics Credential</p>
                        <QRCode
                            size={256}
                            xlinkTitle="dd"
                            style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                            value={data}
                            viewBox={`0 0 256 256`}
                        />
                        <Textarea maxRows={6} value={data}></Textarea>
                    </ModalDialog>
                </Modal>


                <Modal open={goverm_id_ask} onClose={() => set_goverm_id_ask(false)}>
                    <ModalOverflow>
                        <ModalDialog sx={{ width: '30%' }}>
                            <div className="">
                                <p className="text-xl font-semibold my-4  h-fit" >Ask For credential</p>
                                <p>From</p>
                                <Select onChange={(event: React.SyntheticEvent | null,
                                    newValue: string | null,) => {
                                    set_asked_peer(newValue)
                                }} >
                                    {
                                        peers.map((value: any, index: number) => {
                                            return (<Option className="truncate w-[400px]" value={value["peers"]["their_did"]} key={value["peers"]["connection_id"]} >{value["peers"]["their_did"]}</Option>);
                                        })
                                    }
                                </Select>
                                <Button onClick={async () => {

                                    if (asked_peer.trim().length > 0) {
                                        let _d = await axios.post(`http://localhost:5000/ask_presentation/biometrics/${asked_peer}`);
                                        console.log(_d)

                                        setActiveStep(1)
                                        set_goverm_id_ask(false)
                                    }

                                }} className="w-full" sx={{ borderRadius: '100px', mt: '32px' }} variant="soft" >Send Credential Request</Button>
                            </div>
                        </ModalDialog>
                    </ModalOverflow>
                </Modal>


                <Modal open={is_did_doc_open} onClose={() => set_did_doc_open(false)}>
                    <ModalOverflow>
                        <ModalDialog sx={{ width: '30%' }}>
                            <div className="">
                                <p className="text-xl font-semibold my-4  h-fit" >Did Document</p>
                                {
                                    did_doc ? (<JsonView data={did_doc['didDocument']}></JsonView>) : (<p>Hello</p>)
                                }


                            </div>
                        </ModalDialog>
                    </ModalOverflow>
                </Modal>

            </div>
        </div>
    )
}