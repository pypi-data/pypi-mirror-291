"use strict";
(self["webpackChunkpresentpy_jupyter"] = self["webpackChunkpresentpy_jupyter"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);

// import { requestAPI } from './handler';

// import { ToolbarButton } from '@jupyterlab/apputils';
// import { downloadIcon } from '@jupyterlab/ui-components';

/**
 * Initialization data for the presentpy_jupyter extension.
 */
const plugin = {
    id: 'presentpy_jupyter:plugin',
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, settingRegistry, notebooks) => {
        console.log('JupyterLab extension presentpy_jupyter is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('presentpy_jupyter settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for presentpy_jupyter.', reason);
            });
        }
        const { commands } = app;
        const command = 'presentpy_jupyter:convert';
        // Add a command
        commands.addCommand(command, {
            label: 'ODP',
            caption: 'Export to ODP',
            execute: async (args) => {
                var _a;
                const extensionSettings = await (settingRegistry === null || settingRegistry === void 0 ? void 0 : settingRegistry.load(plugin.id));
                const path = (_a = notebooks.currentWidget) === null || _a === void 0 ? void 0 : _a.sessionContext.path;
                const orig = args['origin'];
                if (orig !== 'init') {
                    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
                    const requestUrl = `${settings.baseUrl}presentpy-jupyter/download`;
                    try {
                        const theme = (extensionSettings === null || extensionSettings === void 0 ? void 0 : extensionSettings.get('theme').composite) ||
                            'default';
                        const keep_odp = (extensionSettings === null || extensionSettings === void 0 ? void 0 : extensionSettings.get('keep_odp').composite) ||
                            false;
                        console.log(`Converting ${path} to ODP with theme ${theme} and keep_odp ${keep_odp}`);
                        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, {
                            method: 'POST',
                            body: JSON.stringify({
                                path: path,
                                theme: theme,
                                keep_odp: keep_odp
                            })
                        }, settings);
                        if (response.status !== 200) {
                            const data = await response.json();
                            throw new Error(data.message || 'Unknown error');
                        }
                        const notebook_name = (path === null || path === void 0 ? void 0 : path.split('/').pop()) || 'notebook.ipynb';
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `${notebook_name.split('.')[0]}.odp`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(url);
                    }
                    catch (error) {
                        console.error('Failed to download notebook:', error);
                    }
                }
            }
        });
        // Call the command execution
        commands.execute(command, { origin: 'init' }).catch(reason => {
            console.error(`An error occurred during the execution of jlab-examples:command.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.fdfbc9f970aa548f8e68.js.map