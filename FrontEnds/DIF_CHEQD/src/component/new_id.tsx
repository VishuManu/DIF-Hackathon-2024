import React, { useState } from "react";
import { Box, Button, DialogContent, FormControl, FormLabel, Input, Modal, ModalClose, ModalDialog, Option, Radio, RadioGroup, Select, Textarea } from "@mui/joy";
import { cred_status, cred_status_index, cred_status_index_suspense, holder, issuer_gov } from "./VARS";
import axios from "axios";
import QRCode from "react-qr-code";


export default function NEW() {
    const [formData, setFormData] = useState({
        fullName: '',
        dob: '',
        gender: '',
        address: '',
        city: '',
        state: '',
        zipCode: '',
        idNumber: '',
        nationality: '',
        issueDate: '',
        expirationDate: '',
        photo: null,
        signature: '',
    });

    const [open, set_open] = useState(false)
    const [data, set_data] = useState("")

    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
        console.log(formData)
    };

    const handleFileChange = (e: any) => {
        setFormData((prev) => ({ ...prev, [e.target.name]: e.target.files[0] }));
    };

    const handleSubmit = (e: any) => {
        e.preventDefault();
        // Handle form submission logic here
        console.log('Form Submitted:', formData);
    };
    async function create_json_ld() {
        const _w3c_json = {
            "@context": ["https://www.w3.org/ns/credentials/v2"],
            "id": "AZXC",
            "type": ["VerifiableCredential","GovermentIdCredential"],
            "issuer": issuer_gov,
            "validFrom": formData.issueDate,
            "validUntil": formData.expirationDate,
            "credentialSubject": {
                "id": holder,
                "fullName": formData.fullName,
                "gender": formData.gender,
                "dateOfBirth": formData.dob,
                "nationality": formData.nationality,
                "address": {
                    "streetAddress": formData.address,
                    "city": formData.city,
                    "state": formData.state,
                    "postalCode": formData.zipCode,
                },
                "governmentIDNumber": formData.idNumber,
            },
            "credentialStatus": [{
                "id": cred_status,
                "type": "StatusList2021Entry",
                "statusPurpose": "revocation",
                "statusListIndex": cred_status_index,
            }, {
                "id": cred_status,
                "type": "StatusList2021Entry",
                "statusPurpose": "suspension",
                "statusListIndex": cred_status_index_suspense,
            }]

        }
        const ax = await axios.post(`http://localhost:3000/get_sd_jwt`, _w3c_json)
        if (ax.status == 200) {
            set_open(true)
            set_data(ax.data)
            console.log(ax)
        }
    }
    return (
        <div className="px-[30%] col-span-1 pb-16">
            <p className="font-mono font-bold text-2xl py-8" >Issue Goverment Id</p>
            <div
                onSubmit={handleSubmit}
                className="font-mono flex flex-col gap-2 "
            >

                {/* Full Name */}
                <FormControl>
                    <FormLabel>Full Name</FormLabel>
                    <Input
                        placeholder="Enter your full name"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                {/* Date of Birth */}
                <FormControl>
                    <FormLabel>Date of Birth</FormLabel>
                    <Input
                        type="date"
                        name="dob"
                        value={formData.dob}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                {/* Gender */}
                <FormControl>
                    <FormLabel>Gender</FormLabel>
                    <Select
                        name="nationality"
                        value={formData.gender}
                        onChange={(event, ne: any) => {
                            const df = { ...formData };
                            df.gender = ne;
                            setFormData(df)
                        }}
                        required
                    >
                        <Option value="Male">Male</Option>
                        <Option value="Female">Female</Option>
                        <Option value="Other">Other</Option>
                    </Select>
                </FormControl>

                {/* Address */}
                <FormControl>
                    <FormLabel>Street Address</FormLabel>
                    <Input
                        placeholder="Street Address"
                        name="address"
                        value={formData.address}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                <Box sx={{ display: 'flex', gap: 2 }}>
                    <FormControl sx={{ flex: 1 }}>
                        <FormLabel>City</FormLabel>
                        <Input
                            placeholder="City"
                            name="city"
                            value={formData.city}
                            onChange={handleChange}
                            required
                        />
                    </FormControl>

                    <FormControl sx={{ flex: 1 }}>
                        <FormLabel>State</FormLabel>
                        <Input
                            placeholder="State"
                            name="state"
                            value={formData.state}
                            onChange={handleChange}
                            required
                        />
                    </FormControl>
                </Box>

                <FormControl>
                    <FormLabel>Zip Code</FormLabel>
                    <Input
                        placeholder="Zip Code"
                        name="zipCode"
                        value={formData.zipCode}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                {/* Identification Number */}
                <FormControl>
                    <FormLabel>ID Number</FormLabel>
                    <Input
                        placeholder="Enter ID Number"
                        name="idNumber"
                        value={formData.idNumber}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                {/* Nationality */}
                <FormControl>
                    <FormLabel>Nationality</FormLabel>
                    <Select
                        name="nationality"
                        value={formData.nationality}
                        onChange={(event, ne: any) => {
                            const df = { ...formData };
                            df.nationality = ne;
                            setFormData(df)
                        }}
                        required
                    >
                        <Option value="American">American</Option>
                        <Option value="Canadian">Canadian</Option>
                        <Option value="Other">Other</Option>
                    </Select>
                </FormControl>

                {/* Issue Date */}
                <FormControl>
                    <FormLabel>Issue Date</FormLabel>
                    <Input
                        type="date"
                        name="issueDate"
                        value={formData.issueDate}
                        onChange={handleChange}
                        required
                    />
                </FormControl>

                {/* Expiration Date */}
                <FormControl>
                    <FormLabel>Expiration Date</FormLabel>
                    <Input
                        type="date"
                        name="expirationDate"
                        value={formData.expirationDate}
                        onChange={handleChange}
                        required
                    />
                </FormControl>




                {/* Submit Button */}
                <Button onClick={() => {
                    create_json_ld()
                }} sx={{ marginTop: '16px' }} color="primary">
                    Publish                </Button>
            </div>
            <Modal open={open} onClose={() => set_open(false)}>
                <ModalDialog sx={{ width: '30%' }} size='lg'>
                    <ModalClose />
                    <p>Claim Goverment Identity</p>
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
        </div>
    );
}