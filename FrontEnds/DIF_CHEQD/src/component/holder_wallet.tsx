import { Button, Checkbox, Divider, Input, Modal, ModalClose, ModalDialog, Textarea } from "@mui/joy";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { get } from "http";
import { json } from "stream/consumers";
import { Fab } from "@mui/material";
import { Add, Check, CheckCircle, NavigateBefore } from "@mui/icons-material";
import { Base64 } from 'js-base64';
import { ModalOverflow } from '@mui/joy';
import QRCode from "react-qr-code";
import { JsonView, allExpanded, darkStyles, defaultStyles } from 'react-json-view-lite';

export default function Wallet() {
    const [data, set_data] = useState<any[]>([])
    const [open, set_open] = useState(false);
    const [open_present, set_open_present] = useState(false);
    const [selected, set_selected] = useState<any>({})
    const [detail, set_detail] = useState(false);
    const [current_cred, set_current_cred] = useState<any>()
    const [sd_jwt, set_sd_jwt] = useState("")
    const [raw_jwt, set_raw_jwt] = useState("")
    const [invitation_url, set_invitation_url] = useState("")
    const [new_connection, set_new_connection] = useState(false)
    const [is_send, set_is_send] = useState(false)
    const [qr_code, set_qr_code] = useState(false)
    const [give_credential, set_give_credential] = useState(false)
    const [ask, set_asks] = useState([])
    const [cred_request, set_cred_request] = useState({})
    const [show_presentation, set_show_presentation] = useState<any>(null)
    async function save_data() {
        const _d = await axios.post('http://localhost:5003/create')
        if (_d.status == 200) {
            window.location.reload()
        }
        else {
            alert(_d.status + "Error Code")
        }

    }
    function processed_sending_jwt(_payload: Array<string>, _disc: Array<string>) {
        const _signature = _payload[2]?.split('~')[0]
        return `${_payload[0]}.${_payload[1]}.${_signature}~${_disc.join('~')}`

    }

    function processed_last_presentation() {

    }
    useEffect(() => {
        async function get_data() {
            const _d = await axios.get('http://localhost:5003/is_exsist')
            if (typeof (_d.data) === "string") {
                const jsonString = _d.data.replace(/'/g, '"');
                const resultArray = JSON.parse(jsonString);
                set_data(resultArray)
            }
            else {
                set_data(_d.data)
            }

        }

        get_data()
        console.log(data)
    }, [])

    return (
        <div className="grid grid-cols-3">
            <div className="col-span-1">
                <p className="font-semibold px-24 py-4" >Notification</p>
                <div className="flex flex-col px-24">
                    {
                        data[0]?.request?.map((value: any, index: number) => {
                            return (
                                <div className="border bg-zinc-50 rounded-md  px-6 py-4 text-sm font-mono">
                                    <p className="w-full font-bold truncate"> {value['data']["from"]} </p>
                                    <p className="w-full truncate">Ask Your Credentials</p>

                                    <Button onClick={async () => {
                                        set_cred_request(value['data'])
                                        console.log(cred_request?.input_descriptors?.[0]?.constraints)
                                        const f = await axios.post("http://localhost:5001/get_credential", cred_request?.input_descriptors?.[0]?.constraints)

                                        set_asks(f.data)
                                        set_give_credential(true)

                                    }} variant="soft" sx={{ borderRadius: '100px', mt: '16px' }} >Accept</Button>

                                </div>
                            )
                        })
                    }
                </div>
            </div>
            <div className="col-span-1 h-screen border-x bg-white w-full" >
                <div className="w-full bg-zinc-50 border border-b h-fit flex flex-row pb-4 justify-between px-12">
                    <div className="flex flex-row">

                        <div className="flex flex-row gap-8">
                            {
                                data.length > 0 && (
                                    <div onClick={() => {
                                        set_open(true)
                                    }} className="rounded-full cursor-pointer  mt-4 w-fit h-fit ">
                                        <Add sx={{ color: 'black', fontSize: '24px' }} ></Add>

                                    </div>
                                )
                            }
                            <p className="text-black text-xl font-semibold pt-4" >Wallet</p>
                        </div>

                    </div>
                    {
                        data.length > 0 && (
                            <p className="bg-zinc-100 max-w-[250px] overflow-hidden mt-5 whitespace-nowrap text-ellipsis border text-xs h-fit w-fit text-zinc-900 rounded-full px-4 py-0.5 font-bold mt-2" >{data[0]['pub_key']}</p>

                        )
                    }
                </div>
                <div className="lg:xl:px-12 px-8 py-8">
                    {
                        data.length > 0 ? (
                            data[0]["creds"].map((xc: any, index: number) => {
                                return (
                                    <div onClick={() => {
                                        set_current_cred(xc)
                                        //set_raw_jwt(xc['raw']['data'].split('.'))
                                        set_detail(true)
                                    }} className="w-full hover:bg-zinc-50 shadow-lg border rounded-lg ">
                                        <div className="flex flex-row gap-1  rounded-t-lg px-4 py-4">
                                            {
                                                xc["w3c"]["type"].map((xc: any, index: number) => {
                                                    return (
                                                        <p className="font-semibold text-blue-800 font-sans text-sm border border-blue-200 w-fit rounded-full px-3 bg-blue-100" >
                                                            {xc}
                                                        </p>
                                                    )
                                                })
                                            }

                                        </div>
                                        <Divider></Divider>
                                        <div className="grid grid-cols-1 gap-2 mt-4 px-4 pb-4">
                                            <p className="py-2"><span className="font-bold" >Issuer</span> : <span onClick={() => {
                                                window.open(`https://resolver.cheqd.net/1.0/identifiers/${xc["w3c"]["issuer"]}`, "_blank")
                                            }} className="underline text-blue-500 cursor-pointer" >{xc["w3c"]["issuer"]}</span></p>
                                            {
                                                xc["type"] == "ZKP" ? (
                                                    <div >
                                                        <div className="border-yellow-300 px-4 py-2 rounded-lg border-2 border-dashed bg-yellow-100">
                                                            <p className="text-yellow-700 font-bold">ZKP Credential</p>
                                                            <p className="text-yellow-500 text-sm font-semibold">This Credential Contains A ZKP Proof for proof of personhood</p>

                                                        </div>
                                                    </div>
                                                ) : (xc["disc"].map((vl: any, index: number) => {
                                                    return (
                                                        <div className="flex flex-row font-mono gap-3 text-sm" >
                                                            <p className="font-semibold" >{(Base64.decode(vl)).replace(/[\[\]']+/g, '').split(",")[1]}</p>
                                                            <p className="text-zinc-700" >{(Base64.decode(vl)).replace(/[\[\]']+/g, '').split(",")[2]}</p>

                                                        </div>
                                                    )
                                                }))

                                            }




                                        </div>

                                        <div className="flex flex-col  rounded-b-lg px-4 py-2">

                                        </div>
                                    </div>
                                )
                            })
                        ) : (<div className="w-full flex flex-col justify-end  h-full" >
                            <center>
                                <Fab onClick={() => {
                                    save_data()
                                }} className="hover:bg-[#3b82f6]" color="primary" sx={{ width: 'fit-content', color: 'white', fontWeight: 'bold' }} variant="extended" >
                                    <Add sx={{ mr: 1 }} />
                                    Create Wallet
                                </Fab>
                            </center>
                        </div>)
                    }


                </div>
                <center>
                    <Fab onClick={() => {
                        set_new_connection(true)
                    }} className="hover:bg-[#3b82f6]" color="primary" sx={{ width: 'fit-content', color: 'white', fontWeight: 'bold' }} variant="extended" >
                        <Add sx={{ mr: 1 }} />
                        Create Connection
                    </Fab>
                </center>
                <Modal open={open} onClose={() => set_open(false)}>
                    <ModalDialog sx={{ width: '30%', height: '35%' }} size='lg'>
                        <ModalClose />
                        <p className="-mt-2 font-bold">Add New Credential</p>
                        <form onSubmit={() => {
                            async function processed(id: string, _data: string) {
                                const aw = await axios.post('http://localhost:5003/validate', {
                                    data: sd_jwt,
                                    my_key: data[0]['pub_key']
                                })

                            }


                            processed("test", "asddh")
                        }}>
                            <Textarea sx={{ marginBottom: '16px' }} required onChange={(event) => {
                                set_sd_jwt(event.target.value)
                            }} placeholder="SD-JWT Credential" minRows={8} maxRows={8}></Textarea>
                            <Button className="w-full" type="submit" variant="soft" >Validate Credential</Button>
                        </form>
                    </ModalDialog>
                </Modal>
                <Modal open={detail} onClose={() => set_detail(false)}>
                    <ModalOverflow>
                        <ModalDialog sx={{ height: '' }} >
                            <ModalClose />
                            <div className="max-w-xl mx-auto">
                                <p className="text-2xl font-semibold my-4  h-fit" >Credential</p>

                                <JsonView data={current_cred} shouldExpandNode={allExpanded} style={defaultStyles} />

                                <Button onClick={() => {
                                    set_open_present(true)
                                }} className="w-full" sx={{ borderRadius: '100px', mt: '32px' }} >Send/Present Credential</Button>
                            </div>
                        </ModalDialog>
                    </ModalOverflow>
                </Modal>

                <Modal open={qr_code} onClose={() => set_qr_code(false)}>
                    <ModalDialog sx={{ width: '30%' }} size='lg'>
                        <ModalClose />
                        <p>Send SD-JWT To Verifier</p>

                        <Textarea maxRows={6} value={raw_jwt && (processed_sending_jwt(raw_jwt, []))}></Textarea>
                    </ModalDialog>
                </Modal>
                <Modal open={new_connection} onClose={() => set_new_connection(false)}>
                    <ModalDialog sx={{ width: '30%' }} size='lg'>
                        <ModalClose />
                        <p>New Connection</p>

                        <Input onChange={(event) => {
                            set_invitation_url(event.target.value)
                        }} placeholder="Enter Invitation URL" ></Input>
                        <center>
                            <Fab onClick={async () => {
                                const aw = await axios.post("http://localhost:5001/accept", {
                                    "url": invitation_url,
                                    "my_key": data[0]['pub_key']
                                })
                                console.log(aw)

                                if (aw.status == 200) {
                                }
                            }} className="hover:bg-[#3b82f6]" size="small" color="primary" sx={{ width: 'fit-content', color: 'white', fontWeight: 'bold' }} variant="extended" >
                                <Add sx={{ mr: 1 }} />
                                Accept Invitation
                            </Fab>
                        </center>
                    </ModalDialog>
                </Modal>


            </div>

            <div className="col-span-1">
                <p className="font-semibold px-24 py-4" >Peer Connection</p>
                <div className="px-24 py-2 flex flex-col" >
                    {
                        data[0]?.peers?.map((value: any, index: number) => {
                            return (
                                <div className="border bg-zinc-50 rounded-md  px-6 py-4 text-sm font-mono">
                                    <p className="w-full truncate"> <span className="font-bold ">➤ Connection Id</span> : {value['connection_id']}</p>

                                    <p className="w-full truncate"> <span className="font-bold ">➤ My Peer</span> : {value["my_did"]}</p>
                                    <p className="w-full truncate"> <span className="font-bold ">➤ Other Peer</span> : {value["their_did"]}</p>

                                </div>
                            )
                        })
                    }



                </div>
            </div>

            <Modal open={give_credential} onClose={() => set_give_credential(false)}>
                <ModalOverflow>
                    <ModalDialog sx={{ width: '30%' }}>
                        <div className="">
                            <p className="text-xl font-semibold my-4  h-fit" >Ask For credential</p>
                            <div className="flex flex-col">
                                <p><span className="font-bold" >Request</span>  : {cred_request?.input_descriptors?.[0]?.name}</p>
                                <p><span className="font-bold" >Purpose</span>  : {cred_request?.input_descriptors?.[0]?.purpose}</p>
                                <p className="w-full truncate" ><span className="font-bold" >From</span> : {cred_request?.from}</p>
                                <p className="text-xl underline underline-offset-4 decoration-dashed decoration-zinc-300 mt-8 " >Available Credential</p>
                                <p className="text-xs mb-8">These are the credential present on the wallet that satisfy constrain provioded by issuer</p>
                                {
                                    data?.[0]?.['creds'].length > 0 ?
                                        (
                                            data?.[0]?.['creds'].map((value: any, index: number) => {
                                                let w3c = value['w3c']
                                                if (ask.includes(w3c['id'])) {
                                                    return (
                                                        <div className="w-full hover:bg-zinc-50 shadow-lg border rounded-lg ">
                                                            <div className="flex flex-row gap-1  rounded-t-lg px-4 py-4">
                                                                {
                                                                    w3c["type"].map((xc: any, index: number) => {
                                                                        return (
                                                                            <p className="font-semibold text-blue-800 font-sans text-sm border border-blue-200 w-fit rounded-full px-3 bg-blue-100" >
                                                                                {xc}
                                                                            </p>
                                                                        )
                                                                    })
                                                                }

                                                            </div>
                                                            <Divider></Divider>
                                                            <div className="grid grid-cols-1 gap-2 mt-4 px-4 pb-4">
                                                                <p className="py-2"><span className="font-bold" >Issuer</span> : <span onClick={() => {
                                                                    window.open(`https://resolver.cheqd.net/1.0/identifiers/${w3c["issuer"]}`, "_blank")
                                                                }} className="underline text-blue-500 cursor-pointer" >{w3c["issuer"]}</span></p>
                                                                {
                                                                    value["type"] == "ZKP" ? (
                                                                        <div >
                                                                            <div className="border-yellow-300 px-4 py-2 rounded-lg border-2 border-dashed bg-yellow-100">
                                                                                <p className="text-yellow-700 font-bold">ZKP Credential</p>
                                                                                <p className="text-yellow-500 text-sm font-semibold">This Credential Contains A ZKP Proof for proof of personhood</p>

                                                                            </div>
                                                                        </div>
                                                                    ) : (value["disc"].map((vl: any, index: number) => {
                                                                        return (
                                                                            <div className="flex flex-row font-mono gap-3 text-sm" >
                                                                                <p className="font-semibold" >{(Base64.decode(vl)).replace(/[\[\]']+/g, '').split(",")[1]}</p>
                                                                                <p className="text-zinc-700" >{(Base64.decode(vl)).replace(/[\[\]']+/g, '').split(",")[2]}</p>

                                                                            </div>
                                                                        )
                                                                    }))

                                                                }




                                                            </div>

                                                            <div className="flex flex-col gap-4 pb-8 rounded-b-lg px-4 py-2">
                                                                {
                                                                    value['disc'].map((_vl: any, idx: number) => {
                                                                        return (
                                                                            <Checkbox onChange={(event) => {
                                                                                if (event.target.checked) {
                                                                                    let existing = { ...selected };
                                                                                    let arr = existing[index] || [];
                                                                                    arr.push(_vl);
                                                                                    existing[index] = arr;
                                                                                    set_selected(existing);
                                                                                    console.log(selected)
                                                                                }
                                                                                else {
                                                                                    let existing = { ...selected }
                                                                                    existing[index] = existing[index].filter((value: any) => value != _vl)
                                                                                    set_selected(existing)
                                                                                    console.log(selected)

                                                                                }
                                                                            }} label={(Base64.decode(_vl))?.replace(/[\[\]']+/g, '').split(",")[1]} variant="outlined" value={value} />

                                                                        )
                                                                    })
                                                                }
                                                            </div>
                                                        </div>
                                                    )
                                                }
                                            })
                                        ) : (<div>
                                            No Credential
                                        </div>)
                                }

                            </div>
                            {
                                show_presentation && (
                                    <JsonView data={show_presentation}></JsonView>
                                )
                            }
                            <Button onClick={async () => {
                                let envelops_presentation: any[] = []
                                let type = ""
                                data?.[0]?.['creds'].length > 0 && (
                                    data?.[0]?.['creds'].map((value: any, index: number) => {
                                        type = value["type"]
                                        if (type !== "ZKP") {
                                            let raw: string = value['raw']['data']
                                            let _main = raw.split('~')[0]
                                            _main = `${_main}~${selected[index].join('~')}`
                                            envelops_presentation.push(_main)
                                        }
                                        else {
                                            envelops_presentation.push(value["w3c"])
                                        }

                                    })
                                )
                                let verifiablePresentation: any = type == "ZKP" ? {
                                    "request_id": cred_request?.input_descriptors?.[0]?.id,
                                    "from": cred_request?.from,
                                    "cred": {
                                        "@context": [
                                            "https://www.w3.org/ns/credentials/v2",
                                            "https://www.w3.org/ns/credentials/examples/v2"
                                        ],
                                        "type": ["VerifiablePresentation", "PersonHoodPresentation"],
                                        "id": "urn:uuid:313801ba-24b7-11ee-be02-ff560265cf9b",
                                        "verifiableCredential": envelops_presentation.map((value: string, index: number) => {
                                            return (
                                                { value }
                                            )
                                        }),
                                    }
                                } : {
                                    "request_id": cred_request?.input_descriptors?.[0]?.id,
                                    "from": cred_request?.from,
                                    "cred": {
                                        "@context": [
                                            "https://www.w3.org/ns/credentials/v2",
                                            "https://www.w3.org/ns/credentials/examples/v2"
                                        ],
                                        "type": ["VerifiablePresentation"],
                                        "id": "urn:uuid:313801ba-24b7-11ee-be02-ff560265cf9b",
                                        "verifiableCredential": envelops_presentation.map((value: string, index: number) => {
                                            return (
                                                {
                                                    "@context": "https://www.w3.org/ns/credentials/v2",
                                                    "id": `data:application/vc+sd-jwt,${value}`,
                                                    "type": "EnvelopedVerifiableCredential",

                                                }
                                            )
                                        }),
                                    }
                                }
                                const _signature = await axios.post("http://localhost:5003/sign", {
                                    "payload": verifiablePresentation
                                })
                                verifiablePresentation["proof"] = {
                                    "type": "DataIntegrityProof",
                                    "cryptosuite": "eddsa-rdfc-2022",
                                    "created": "2021-11-13T18:19:39Z",
                                    "verificationMethod": "https://university.example/issuers/14#key-1",
                                    "proofPurpose": "assertionMethod",
                                    "proofValue": _signature.data,
                                }
                                const _req = await axios.post('http://localhost:5001/send_presentation', verifiablePresentation)
                                if (_req.status == 200)
                                    set_show_presentation(verifiablePresentation)
                                

                            }} className="w-full" sx={{ borderRadius: '100px', mt: '32px' }} variant="soft" >Send Selective Disclosure Credential</Button>

                            {
                                is_send && (
                                    <center className="my-6">
                                        <CheckCircle sx={{ color: 'green' }}></CheckCircle>

                                    </center>
                                )
                            }
                        </div>
                    </ModalDialog>
                </ModalOverflow>
            </Modal>

        </div>
    )
}