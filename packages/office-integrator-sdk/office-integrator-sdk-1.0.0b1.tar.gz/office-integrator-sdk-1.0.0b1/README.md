# Zoho Office Integrator Python SDK
* [Getting Started](#Getting-Started)
* [Registering a Zoho Office Integrator APIKey](#registering-a-zoho-office-integrator-apikey)
* [Environmental Setup](#environmental-setup)
* [Including the SDK in your project](#including-the-sdk-in-your-project)
* [Sample Code](#sdk-sample-code)
* [Release Notes](#release-notes)
* [License](#license)

## Getting Started

Zoho Office Integrator Pythod SDK used to help you quickly integrator Zoho Office Integrator editors in side your web application.

* [Python SDK Source code](https://github.com/zoho/office-integrator-python-sdk)
* [API reference documentation](https://www.zoho.com/officeintegrator/api/v1)
* [SDK example code](https://github.com/zoho/office-integrator-python-sdk-examples)

## Registering a Zoho Office Integrator APIKey

Since Zoho Office Integrator APIs are authenticated with apikey, you should register your with Zoho to get an apikey. To register your app:

- Visit this page [https://officeintegrator.zoho.com/](https://officeintegrator.zoho.com). ( Sign-up for a Zoho Account if you don't have one)

- Enter your company name and short discription about how you are going to using zoho office integrator in your application. Choose the type of your application(commerial or non-commercial) and generate the apikey.

- After filling above details, create an account in Zoho Office Integrator service and copy the apikey from the dashboard.

## Environmental Setup

- Python 3.8 or later is required to use this package.

- Python SDK must be installed into client app through **pip**.

## Including the SDK in your project

You can include the SDK to your project using:

- Install **Python SDK**
    - Navigate to the workspace of your client app.
    - Run the command below:

    ```sh
    pip install office-integrator-sdk
    ```

- Another method to install the SDK
    - Add following line in requirements.txt file of your application.
    
     ```sh
    office-integrator-sdk==1.0.2
    ```
    - Run the follwoing comment install the sdk files
     ```sh
    pip3 install -r requirements.txt
    ```

## SDK Sample code

Refer this **[repository](https://github.com/zoho/office-integrator-python-sdk-examples)** for example codes to all Office Integrator API endpoints.

## Release Notes

*Version 1.0.b1*

- Initial sdk version release

## License

This SDK is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0), see LICENSE.txt for more information.
