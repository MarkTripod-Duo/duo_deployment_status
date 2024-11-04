# Cisco Duo Production Deployment Status Tracking
This repository contains an example of how to monitor the operational status of various components of the Cisco Duo production environment. 

## Installation

`#pip -r requirements.txt`

## Usage

`#python3 duo_deployment_status.py <Duo Deployment ID>`

### Example

```python
> python3 duo_deployment_status.py duo63
DUO63 status: operational
Core Authentication Service status: operational
Admin Panel status: operational
Push Delivery status: operational
Phone Call Delivery status: operational
SMS Message Delivery status: operational
Cloud PKI status: operational
SSO status: operational
```
