var FindProxyForURL = function(init, profiles) {
    return function(url, host) {
        "use strict";
        var result = init, scheme = url.substr(0, url.indexOf(":"));
        do {
            result = profiles[result];
            if (typeof result === "function") result = result(url, host, scheme);
        } while (typeof result !== "string" || result.charCodeAt(0) === 43);
        return result;
    };
}("+auto switch", {
    "+auto switch": function(url, host, scheme) {
        "use strict";
        if (/ec2.*\.amazonaws\.com/.test(host)) return "+proxy";
        if (/ec2.*\.compute/.test(host)) return "+proxy";
        if (/^http:\/\/10\.200\./.test(url)) return "+proxy";
        if (/10.*\.amazonaws\.com/.test(host)) return "+proxy";
        if (/10-200.*\.compute/.test(host)) return "+proxy";
        if (/(?:^|\.)compute\.internal/.test(host)) return "+proxy";
        if (/(?:^|\.)ec2\.internal/.test(host)) return "+proxy";
        return "DIRECT";
    },
    "+proxy": function(url, host, scheme) {
        "use strict";
        if (/^127\.0\.0\.1$/.test(host) || /^::1$/.test(host) || /^localhost$/.test(host)) return "DIRECT";
        return "SOCKS5 localhost:8157; SOCKS localhost:8157";
    }
});