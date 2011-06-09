/*!
 * This file is part of Aloha Editor
 * Author & Copyright (c) 2010 Gentics Software GmbH, aloha@gentics.com
 * Licensed unter the terms of http://www.aloha-editor.com/license.html
 */

/*
 * The GENTICS global namespace object. If GENTICS is already defined, the
 * existing GENTICS object will not be overwritten so that defined
 * namespaces are preserved.
 */
var Aloha = window.Aloha;
// before closure (for loading)
Aloha = jQuery.extend(Aloha,{
	
});

// Start Closure
(function(window, undefined) {
	// Namespace jQuery
	window.alohaQuery = window.jQuery; // window.jQuery.sub();

        // emulate document.head support for browsers that do not have it
        document.head = document.head || document.getElementsByTagName('head')[0];

	// Prepare
	var
		jQuery = window.alohaQuery, $ = jQuery,
		GENTICS = window.GENTICS,
		Aloha = window.Aloha;

	/**
	 * Base Aloha Object
	 * @namespace Aloha
	 * @class Aloha The Aloha base object, which contains all the core functionality
	 * @singleton
	 */
	Aloha = jQuery.extend(true,Aloha,{

		/**
		 * The Aloha Editor Version we are using
		 * It should be set by us and updated for the particular branch
		 * @property
		 */
		version: '0.10.0',

		/**
		 * Array of editables that are managed by Aloha
		 * @property
		 * @type Array
		 */
		editables: [],

		/**
		 * The currently active editable is referenced here
		 * @property
		 * @type Aloha.Editable
		 */
		activeEditable: null,

		/**
		 * Flag to mark whether Aloha is ready for use. Will be set at the end of the init() Function.
		 * @property
		 * @type boolean
		 */
		ready: false,

		/**
		 * The aloha dictionaries
		 * @hide
		 */
		dictionaries: {},

		/**
		 * settings object, which will contain all Aloha settings
		 * @cfg {Object} object Aloha's settings
		 */
		settings: {},

		/**
		 * This represents the name of the users OS. Could be:
		 * 'Mac', 'Linux', 'Win', 'Unix', 'Unknown'
		 * @property
		 * @type string
		 */
		OSName: 'Unknown',

		/**
		 * Array of callback functions to call when Aloha is ready
		 * @property
		 * @type Array
		 * @hide
		 */
		readyCallbacks: [],

		/**
		 * Has aloha been initialised?
		 */
		initd: false,

		/**
		 * Initialize Aloha
		 * called automatically by the loader
		 * @event the "ready" event is triggered as soon as Aloha has finished it's initialization process
		 * @hide
		 */
		init: function () {
			// Check
			if ( this.initd ) {
				throw new Error('You are initialising Aloha Editor twice');
			}
			this.initd = true;
			
			// check browser version on init
			// this has to be revamped, as
			if (jQuery.browser.webkit && parseFloat(jQuery.browser.version) < 532.5 || // Chrome/Safari 4
				jQuery.browser.mozilla && parseFloat(jQuery.browser.version) < 1.9 || // FF 3.5
				jQuery.browser.msie && jQuery.browser.version < 7 || // IE 7
				jQuery.browser.opera && jQuery.browser.version < 11 ) { // right now, Opera needs some work
  				if (window.console && console.log) {
                                	console.log('The browser you are using is not supported.');
				}
				return;
			}


			var that = this;

			// register the body click event to blur editables
			jQuery('html').mousedown(function() {
				// if an Ext JS modal is visible, we don't want to loose the focus on
				// the editable as we assume that the user must have clicked somewhere
				// in the modal... where else could he click?
				// loosing the editable focus in this case hinders correct table
				// column/row deletion, as the table module will clean it's selection
				// as soon as the editable is deactivated. Fusubscriberthermore you'd have to
				// refocus the editable again, which is just strange UX
				if (that.activeEditable && !that.isMessageVisible()) {
					that.activeEditable.blur();
					that.FloatingMenu.setScope('Aloha.empty');
					that.activeEditable = null;
				}
			});

			// Initialise the base path to the aloha files
			this.settings.base =
				this.settings.base || window.Aloha_base || this.getAlohaUrl();

			// Initialise pluginDir
			this.settings.pluginDir =
				this.settings.pluginDir || window.Aloha_pluginDir || 'plugin';

			// initialize the Log
			this.Log.init();

			// initialize the error handler for general javascript errors
			if ( this.settings.errorhandling ) {
				window.onerror = function (msg, url, linenumber) {
					Aloha.Log.error(Aloha, 'Error message: ' + msg + '\nURL: ' + url + '\nLine Number: ' + linenumber);
					// TODO eventually add a message to the message line?
					return true;
				};
			}

			// OS detection
			if (navigator.appVersion.indexOf('Win') != -1) {
				this.OSName = 'Win';
			}
			if (navigator.appVersion.indexOf('Mac') != -1) {
				this.OSName = 'Mac';
			}
			if (navigator.appVersion.indexOf('X11') != -1) {
				this.OSName = 'Unix';
			}
			if (navigator.appVersion.indexOf('Linux') != -1) {
				this.OSName = 'Linux';
			}

			// initialize the Aloha core components
			//debugger;
			Aloha.bind('aloha-i18n-ready',this.loadPlugins);
			Aloha.bind('aloha-i18n-plugins-ready', this.loadGui);
			this.initI18n();
			Aloha.bind('aloha-ready', function() {
				Aloha.trigger('aloha');
			});
			
		},
		unbind: function(eventName,eventHandler) {
			eventName = this.correctEventName(eventName);
			$('body').unbind(eventName,eventHandler);
		},

		bind: function(eventName,eventHandler) {
			eventName = this.correctEventName(eventName);
			this.log('debug', this, 'Binding ['+eventName+'], has ['+(($('body').data('events')||{})[eventName]||[]).length+'] events');
			$('body').bind(eventName,eventHandler);
		},

		trigger: function(eventName,data) {
			eventName = this.correctEventName(eventName);
			this.log('debug', this, 'Trigger ['+eventName+'], has ['+(($('body').data('events')||{})[eventName]||[]).length+'] events');
			$('body').trigger(eventName,data);
		},
		correctEventName: function(eventName){
			var result = eventName.replace(/\-([a-z])/g,function(a,b){
				return b.toUpperCase();
			});
			return result;
		},

		/**
		 * Loads plugins that need i18n to be initialized
		 * @return void
		 */
		loadPlugins: function () {
			Aloha.PluginRegistry.init();
		},

		/**
		 * Loads GUI components that need i18n to be initialized
		 * @return void
		 */
		loadGui: function () {
			//debugger;
			Aloha.RepositoryManager.init();
			Aloha.FloatingMenu.init();

			// internationalize ext js message box buttons
			Ext.MessageBox.buttonText.yes = Aloha.i18n(Aloha, 'yes');
			Ext.MessageBox.buttonText.no = Aloha.i18n(Aloha, 'no');
			Ext.MessageBox.buttonText.cancel = Aloha.i18n(Aloha, 'cancel');
			Ext.ux.AlohaAttributeField.prototype.listEmptyText = Aloha.i18n( Aloha, 'repository.no_item_found' );
			Ext.ux.AlohaAttributeField.prototype.loadingText = Aloha.i18n( Aloha, 'repository.loading' ) + '...';

			// set aloha ready
			Aloha.ready = true;

			// activate registered editables
			for (var i = 0, editablesLength = Aloha.editables.length; i < editablesLength; i++) {
				if ( !Aloha.editables[i].ready ) {
					Aloha.editables[i].init();
				}
			}

			Aloha.trigger('aloha-ready');
		},

		/**
		 * Activates editable and deactivates all other Editables
		 * @param {Editable} editable the Editable to be activated
		 * @return void
		 */
		activateEditable: function (editable) {

			// blur all editables, which are currently active
			for (var i = 0, editablesLength = this.editables.length; i < editablesLength; i++) {
				if (this.editables[i] != editable && this.editables[i].isActive) {
					this.editables[i].blur();
				}
			}

			this.activeEditable = editable;
		},

		/**
		 * Returns the current Editable
		 * @return {Editable} returns the active Editable
		 */
		getActiveEditable: function() {
			return this.activeEditable;
		},

		/**
		 * deactivated the current Editable
		 * @return void
		 */
		deactivateEditable: function () {

			if ( typeof this.activeEditable === 'undefined' || this.activeEditable === null ) {
				return;
			}

			// blur the editable
			this.activeEditable.blur();

			// set scope for floating menu
			this.FloatingMenu.setScope('Aloha.empty');

			this.activeEditable = null;
		},

		/**
		 * Gets an editable by an ID or null if no Editable with that ID registered.
		 * @param {string} id the element id to look for.
		 * @return {Aloha.Editable} editable
		 */
		getEditableById: function (id) {

			// if the element is a textarea than route to the editable div
			if (jQuery('#'+id).get(0).nodeName.toLowerCase() === 'textarea' ) {
				id = id + '-aloha';
			}

			// serach all editables for id
			for (var i = 0, editablesLength = Aloha.editables.length; i < editablesLength; i++) {
				if (Aloha.editables[i].getId() == id) {
					return Aloha.editables[i];
				}
			}

			return null;
		},

		/**
		 * Checks wheater an object is a registered Aloha Editable.
		 * @param {jQuery} obj the jQuery object to be checked.
		 * @return {boolean}
		 */
		isEditable: function (obj) {
			for (var i=0, editablesLength = this.editables.length; i < editablesLength; i++) {
				if ( this.editables[i].originalObj.get(0) === obj ) {
					return true;
				}
			}
			return false;
		},

		/**
		 * Logs a message to the console
		 * @param level Level of the log ("error", "warn" or "info", "debug")
		 * @param component Component that calls the log
		 * @param message log message
		 * @return void
		 * @hide
		 */
		log: function(level, component, message) {
			if (typeof Aloha.Log !== "undefined")
				Aloha.Log.log(level, component, message);
		},

		/**
		 * build a string representation of a jQuery or DOM object
		 * @param object to be identified
		 * @return string representation of the object
		 * @hide
		 */
		identStr: function (object) {
			if (object instanceof jQuery) {
				object = object[0];
			}
			if (!(object instanceof HTMLElement)) {
				Aloha.Log.warn(this, '{' + object.toString() + '} provided is not an HTML element');
				return object.toString();
			}

			var out = object.tagName.toLowerCase();

			// an id should be unique, so we're okay with that
			if (object.id) {
				return out + '#' + object.id;
			}

			// as there was no id, we fall back to the objects class
			if (object.className) {
				return out + '.' + object.className;
			}

			// could not identify object by id or class name - so just return the tag name
			return out;
		},

		/**
		 * Initialize i18n, load the dictionary file
		 * Languages may have format as defined in
		 * http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.10
		 * All language codes available http://www.loc.gov/standards/iso639-2/php/langcodes-search.php
		 *
		 * @hide
		 */
		initI18n: function() {

			if (typeof this.settings.i18n === 'undefined' || !this.settings.i18n) {
				this.settings.i18n = {};
			}

			// TODO read dict files automatically on build. Develop only with "en"
			if (typeof this.settings.i18n.available === 'undefined'
				|| !this.settings.i18n.available
				|| !this.settings.i18n.available instanceof Array) {

				this.settings.i18n.available = ['en', 'de', 'fr', 'eo', 'fi', 'ru', 'it', 'pl'];
			}

			/*
			 * try to guess ACCEPT-LANGUAGE from http header
			 * reference http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
			 * ACCEPT-LANGUAGE 'de-de,de;q=0.8,it;q=0.6,en-us;q=0.7,en;q=0.2';
			 * Any implementation has to set it server side because this is not
			 * accessible by JS. http://lists.w3.org/Archives/Public/public-html/2009Nov/0454.html
			*/
			if ( (typeof this.settings.i18n.current === 'undefined' || !this.settings.i18n.current) &&
				typeof this.settings.i18n.acceptLanguage === 'string' ) {

				var acceptLanguage = [],
				// Split the string from ACCEPT-LANGUAGE
					preferredLanguage = this.settings.i18n.acceptLanguage.split(",");
				for(i = 0, languageLength = preferredLanguage.length; i < languageLength; i++) {

					// split language setting
					var lang = preferredLanguage[i].split(';');

					// convert quality to float
					if ( typeof lang[1] === 'undefined' || !lang[1] ) {
						lang[1] = 1;
					} else {
						lang[1] = parseFloat(lang[1].substring(2, lang[1].length));
					}

					// add converted language to accepted languages
					acceptLanguage.push(lang);
				}

				// sort by quality
				acceptLanguage.sort(function (a,b) {return b[1] - a[1];});

				// check in sorted order if any of preferred languages is available
				for(i = 0, languageLength = acceptLanguage.length; i < languageLength; i++) {
					if ( jQuery.inArray(acceptLanguage[i][0], this.settings.i18n.available) >= 0 ) {
						this.settings.i18n.current = acceptLanguage[i][0];
						break;
					}
				}
			}

			/*
			 * default language from for the browser navigator API.
			 */
			if (typeof this.settings.i18n.current == 'undefined' || !this.settings.i18n.current) {
				this.settings.i18n.current = (navigator.language
						? navigator.language       // gecko/webkit/opera
						: navigator.userLanguage   // IE
				);
			}

			// determine the actual language based on current and available languages
			var actualLanguage = this.getLanguage(this.settings.i18n.current, this.settings.i18n.available);

			if (!actualLanguage) {
				Aloha.Log.error(this, 'Could not determine actual language.');
			} else {
				// TODO load the dictionary file for the actual language
				var fileUrl = this.settings.base + '/i18n/' + actualLanguage + '.json';
				this.loadI18nFile(fileUrl, this, function () {
					Aloha.trigger('aloha-i18n-ready');
				});
			}
		},


		/**
		 * Check is language is among available languages
		 * @method
		 * @param {String} language language to be set
		 * @param {Array} availableLanguages list of available languages
		 * @return the actual language as a string
		 */
		getLanguage: function(language, availableLanguages) {

			if (!availableLanguages instanceof Array) {
				Aloha.Log.error(this, 'Available languages must be an Array');
				return null;
			}

			if (typeof language === 'undefined' || !language) {
				return availableLanguages[0];
			}

			for (var i = 0, languagesLength = availableLanguages.length; i < languagesLength; ++i) {
				if (language == availableLanguages[i]) {
					return language;
				}
			}

			return availableLanguages[0];
		},

		/**
		 * parses an i18n file
		 * @param {String} fileUrl
		 * @param {String} component
		 * @hide
		 */
		loadI18nFile: function(fileUrl, component, callback) {
			// Note: this ajax request must be done synchronously, because the otherwise
			// the first i18n calls might come before the dictionary is available
			jQuery.ajax({
				dataType : 'json',
				url : fileUrl,
				error: function(request, textStatus, error) {
					Aloha.Log.error(component, 'Error while getting dictionary file ' + fileUrl + ': server returned ' + textStatus);
					if(typeof callback === 'function') {
						callback.call(component);
					}
				},
				success: function(data, textStatus, request) {
					if (Aloha.Log.isInfoEnabled()) {
						Aloha.Log.info(component, 'Loaded dictionary file ' + fileUrl);
					}
					Aloha.parseI18nFile(data, component);
					if(typeof callback === 'function') {
						callback.call(component);
					}
				}
			});
		},

		/**
		 *
		 * @param data
		 * @param component
		 * @hide
		 */
		parseI18nFile: function(data, component) {
			// Check
			if ( typeof data !== 'object' ) {
				Aloha.Log.warn(component, 'i18n file was not json');
				return false;
			}

			// Save i18n
			this.dictionaries[component.toString()] = data;
		},

		/**
		 * Method to translate the given key for the given component either from the component dictionary, or from the Aloha core library.
		 * @method
		 * @param {String} component component for which the key shall be localized
		 * @param {String} key key to be localized
		 * @param {Array} replacements array of replacements
		 * @return localized string
		 */
		i18n: function(component, key, replacements) {
			var value = null;

			// first get the dictionary for the component
			if (this.dictionaries[component.toString()] && this.dictionaries[component.toString()][key]) {
				value = this.dictionaries[component.toString()][key];
			}

			// when the value was not found and component is not Aloha, do a fallback
			if (!value
				&& component != Aloha
				&& this.dictionaries[Aloha.toString()]
				&& this.dictionaries[Aloha.toString()][key])
			{
				value = this.dictionaries[Aloha.toString()][key];
			}

			// value still not found, so output the key
			if (!value) {
				return '??? ' + key + ' ???';
			} else {
				// substitute placeholders
				if (typeof replacements !== 'undefined' && replacements !== null) {
					for ( var i = 0, repLength = replacements.length; i < repLength; ++i) {
						if (typeof replacements[i] !== 'undefined' && replacements[i] !== null) {
							var regEx = new RegExp('\\{' + (i) + '\\}', 'g'),
								safeArgument = replacements[i].toString().replace(/\{/g, '\\{');
							safeArgument = safeArgument.replace(/\}/g, '\\}');
							value = value.replace(regEx, safeArgument);
						}
					}
				}

				value = value.replace(/\{\d\}/g, '').replace(/\\\{/g, '{').replace(/\\\}/g, '}');
				return value;
			}
		},


		/**
		 * Register the given editable
		 * @param editable editable to register
		 * @return void
		 * @hide
		 */
		registerEditable: function (editable) {
			this.editables.push(editable);
		},

		/**
		 * Unregister the given editable. It will be deactivated and removed from editables.
		 * @param editable editable to unregister
		 * @return void
		 * @hide
		 */
		unregisterEditable: function (editable) {

			// Find the index
			var id = this.editables.indexOf( editable );
			// Remove it if really found!
			if (id != -1) {
				this.editables.splice(id, 1);
			}
		},

		/**
		 * Displays a message according to it's type
		 * @method
		 * @param {Aloha.Message} message the Aloha.Message object to be displayed
		 */
		showMessage: function (message) {

			if (Aloha.FloatingMenu.obj) {
				Aloha.FloatingMenu.obj.css('z-index', 8900);
			}

			switch (message.type) {
				case Aloha.Message.Type.ALERT:
					Ext.MessageBox.alert(message.title, message.text, message.callback);
					break;
				case Aloha.Message.Type.CONFIRM:
					Ext.MessageBox.confirm(message.title, message.text, message.callback);
					break;
				case Aloha.Message.Type.WAIT:
					Ext.MessageBox.wait(message.text, message.title);
					break;
				default:
					this.log('warn', this, 'Unknown message type for message {' + message.toString() + '}');
					break;
			}
		},

		/**
		 * Hides the currently active modal, which was displayed by showMessage()
		 * @method
		 */
		hideMessage: function () {
			Ext.MessageBox.hide();
		},

		/**
		 * checks if a modal dialog is visible right now
		 * @method
		 * @return true if a modal is currently displayed
		 */
		isMessageVisible: function () {
			return Ext.MessageBox.isVisible();
		},

		/**
		 * String representation
		 * @hide
		 */
		toString: function () {
			return 'Aloha';
		},

		/**
		 * Check whether at least one editable was modified
		 * @method
		 * @return {boolean} true when at least one editable was modified, false if not
		 */
		isModified: function () {
			// check if something needs top be saved
			for (var i in this.editables) {
				if (this.editables[i].isModified && this.editables[i].isModified()) {
					return true;
				}
			}

			return false;
		},

		/**
		 * Determines the Aloha Url
		 * @method
		 * @return {String} alohaUrl
		 */
		getAlohaUrl: function(suffix){
			window.Aloha_base = window.Aloha_base || document.getElementById('aloha-script-include').src.replace(/aloha\.js$/,'').replace(/\/+$/,'');
			return window.Aloha_base;
		},

		/**
		 * Gets the Plugin Url
		 * @method
		 * @param {String} pluginName
		 * @return {String} pluginUrl
		 */
		getPluginUrl: function(pluginName){
			var pluginUrl = Aloha.getAlohaUrl() + '/plugin/'+pluginName;
			return pluginUrl;
		},

		/**
		 * Load in a JS File
		 * @method
		 * @param {String} pluginName
		 * @return
		 */
		loadJs: function(url){
			// Prepare
			var scriptEl, appendEl = document.head;

			// Append
			scriptEl = document.createElement('script');
			scriptEl.src = url;
			scriptEl.setAttribute('defer','defer');
			appendEl.appendChild(scriptEl);

			// Chain
			return this;
		},

		/**
		 * Load in a CSS File
		 * @method
		 * @param {String} pluginName
		 * @return
		 */
		loadCss: function(url){
			// Prepare
			var linkEl, appendEl = document.head;

			// Append
			linkEl = document.createElement('link');
			linkEl.type = 'text/css';
			linkEl.rel = 'stylesheet';
			linkEl.href = url;
			appendEl.appendChild(linkEl);

			// Chain
			return this;
		},

		/**
		 * Load in a Plugin
		 * @method
		 * @param {String} pluginName
		 * @return
		 */
		loadPlugin: function(pluginName){
			// Prepare
			var pluginUrl = Aloha.getPluginUrl(pluginName);

			// Check if plugin has already be loaded
			if ( typeof window.Aloha_loaded_plugins[pluginName] !== 'undefined' ) {
				window.Aloha_loaded_plugins[pluginName] = false; // continue
			}
			if (window.Aloha_loaded_plugins[pluginName]) {
				return true;
			}
			window.Aloha_loaded_plugins[pluginName] = true;

			// Prepare Actions
			var actions = {
				/**
				 * Load a Plugin by the Default Structure
				 */
				loadDefault: function(){
					// Prepare
					var
						pluginJsUrl = pluginUrl+'/src/'+pluginName+'.js',
						pluginCssUrl = pluginUrl+'/src/'+pluginName+'.css';

					// Include
					Aloha.loadJs(pluginJsUrl);
					Aloha.loadCss(pluginCssUrl);

					// Done
					return true;
				},

				/**
				 * Load a Plugin by it's specified Package
				 */
				loadPackage: function(data){
					// Cycle through CSS
					$.each(data.css||[], function(i,value){
						Aloha.loadCss(pluginUrl+'/'+value);
					});

					// Cycle through JS
					$.each(data.js||[], function(i,value){
						Aloha.loadJs(pluginUrl+'/'+value);
					});

					// Done
					return true;
				}
			};

			// Load In
			$.ajax({
				url: pluginUrl+'/package.json',
				dataType: 'json',
				success: function(data, textStatus, jqXHR) {
					// package.json exists,

					// Load Package
					if ( typeof data === 'object' && typeof data.js !== 'undefined' ) {
						actions.loadPackage(data);
					}
					else {
						actions.loadDefault();
					}

					// Done
					return true;
				},
				error: function (jqXHR, textStatus, errorThrown) {
					// package.json doesn't exist

					// Load Defaults
					actions.loadDefault();

					// Done
					return true;
				}
			});

			// Done
			return true;
		}
	});


	// Initialise Aloha
//	$(function(){
		// Prepare
//		var $body = $('body');
//		$body.createPromiseEvent('aloha');
		// Give the page 3 seconds to load in all the plugins
		// Looks like a jacky hack - Event programming could result to safe loading process..
//		setTimeout( function() {
//			Aloha.init(); // moving to aloha.js
//		},3000);
//	});

})(window);
