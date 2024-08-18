(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define("/Plugin/jquery-placeholder", ["exports", "jquery", "Plugin"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require("jquery"), require("Plugin"));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.jQuery, global.Plugin);
    global.PluginJqueryPlaceholder = mod.exports;
  }
})(this, function (_exports, _jquery, _Plugin2) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.default = void 0;
  _jquery = babelHelpers.interopRequireDefault(_jquery);
  _Plugin2 = babelHelpers.interopRequireDefault(_Plugin2);
  var NAME = 'placeholder';

  var Placeholder =
  /*#__PURE__*/
  function (_Plugin) {
    babelHelpers.inherits(Placeholder, _Plugin);

    function Placeholder() {
      babelHelpers.classCallCheck(this, Placeholder);
      return babelHelpers.possibleConstructorReturn(this, babelHelpers.getPrototypeOf(Placeholder).apply(this, arguments));
    }

    babelHelpers.createClass(Placeholder, [{
      key: "getName",
      value: function getName() {
        return NAME;
      }
    }, {
      key: "render",
      value: function render() {
        if (!_jquery.default.fn.placeholder) {
          return;
        }

        var $el = this.$el;
        $el.placeholder();
      }
    }], [{
      key: "getDefaults",
      value: function getDefaults() {
        return {};
      }
    }]);
    return Placeholder;
  }(_Plugin2.default);

  _Plugin2.default.register(NAME, Placeholder);

  var _default = Placeholder;
  _exports.default = _default;
});