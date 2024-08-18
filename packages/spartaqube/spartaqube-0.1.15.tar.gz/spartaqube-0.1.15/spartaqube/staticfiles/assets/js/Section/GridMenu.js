(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define("/Section/GridMenu", ["exports", "jquery", "Component"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require("jquery"), require("Component"));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.jQuery, global.Component);
    global.SectionGridMenu = mod.exports;
  }
})(this, function (_exports, _jquery, _Component2) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.default = void 0;
  _jquery = babelHelpers.interopRequireDefault(_jquery);
  _Component2 = babelHelpers.interopRequireDefault(_Component2);
  var $BODY = (0, _jquery.default)('body');
  var $HTML = (0, _jquery.default)('html');

  var Scrollable =
  /*#__PURE__*/
  function () {
    function Scrollable($el) {
      babelHelpers.classCallCheck(this, Scrollable);
      this.$el = $el;
      this.api = null;
      this.init();
    }

    babelHelpers.createClass(Scrollable, [{
      key: "init",
      value: function init() {
        this.api = this.$el.asScrollable({
          namespace: 'scrollable',
          skin: 'scrollable-inverse',
          direction: 'vertical',
          contentSelector: '>',
          containerSelector: '>'
        }).data('asScrollable');
      }
    }, {
      key: "update",
      value: function update() {
        if (this.api) {
          this.api.update();
        }
      }
    }, {
      key: "enable",
      value: function enable() {
        if (!this.api) {
          this.init();
        }

        if (this.api) {
          this.api.enable();
        }
      }
    }, {
      key: "disable",
      value: function disable() {
        if (this.api) {
          this.api.disable();
        }
      }
    }]);
    return Scrollable;
  }();

  var GridMenu =
  /*#__PURE__*/
  function (_Component) {
    babelHelpers.inherits(GridMenu, _Component);

    function GridMenu() {
      var _babelHelpers$getProt;

      var _this;

      babelHelpers.classCallCheck(this, GridMenu);

      for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
        args[_key] = arguments[_key];
      }

      _this = babelHelpers.possibleConstructorReturn(this, (_babelHelpers$getProt = babelHelpers.getPrototypeOf(GridMenu)).call.apply(_babelHelpers$getProt, [this].concat(args)));
      _this.isOpened = false;
      _this.scrollable = new Scrollable(_this.$el);
      return _this;
    }

    babelHelpers.createClass(GridMenu, [{
      key: "open",
      value: function open() {
        this.animate(function () {
          this.$el.addClass('active');
          (0, _jquery.default)('[data-toggle="gridmenu"]').addClass('active').attr('aria-expanded', true);
          $BODY.addClass('site-gridmenu-active');
          $HTML.addClass('disable-scrolling');
        }, function () {
          this.scrollable.enable();
        });
        this.isOpened = true;
      }
    }, {
      key: "close",
      value: function close() {
        this.animate(function () {
          this.$el.removeClass('active');
          (0, _jquery.default)('[data-toggle="gridmenu"]').addClass('active').attr('aria-expanded', true);
          $BODY.removeClass('site-gridmenu-active');
          $HTML.removeClass('disable-scrolling');
        }, function () {
          this.scrollable.disable();
        });
        this.isOpened = false;
      }
    }, {
      key: "toggle",
      value: function toggle(opened) {
        if (opened) {
          this.open();
        } else {
          this.close();
        }
      }
    }, {
      key: "animate",
      value: function animate(doing, callback) {
        var _this2 = this;

        doing.call(this);
        this.$el.trigger('changing.site.gridmenu');
        setTimeout(function () {
          callback.call(_this2);

          _this2.$el.trigger('changed.site.gridmenu');
        }, 500);
      }
    }]);
    return GridMenu;
  }(_Component2.default);

  var _default = GridMenu;
  _exports.default = _default;
});