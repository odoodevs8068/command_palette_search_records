/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import {
    CommandPalette,
    splitCommandName,
} from "@web/core/commands/command_palette";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(CommandPalette.prototype, {

    setup() {
        super.setup();

        this.orm = useService("orm");
        this.action = useService("action");

        this.recordSearchSequence = 0;
        this.recordSearchTimer = null;
    },

    async searchRecords(searchValue) {
        searchValue = (searchValue || "").trim();

        if (!searchValue || searchValue.length < 2) {
            return [];
        }

        if (this.recordSearchTimer) {
            clearTimeout(this.recordSearchTimer);
            this.recordSearchTimer = null;
        }

        const sequence = ++this.recordSearchSequence;

        await new Promise((resolve) => {
            this.recordSearchTimer = setTimeout(() => {
                this.recordSearchTimer = null;
                resolve();
            }, 250);
        });

        if (sequence !== this.recordSearchSequence) {
            return [];
        }

        const records = await this.orm.call(
            "command.palette.record.search",
            "search_records",
            [searchValue]
        );

        if (sequence !== this.recordSearchSequence) {
            return [];
        }

        return records.map((record) => {
            const name = `${record.description} / ${record.name}`;

            return {
                name,
                category: "records",
                keyId: this.keyId++,
                splitName: splitCommandName(
                    name,
                    searchValue
                ),
                recordId: record.id,
                recordModel: record.model,

                action: async () => {
                    await this.action.doAction({
                        type: "ir.actions.act_window",
                        res_model: record.model,
                        res_id: record.id,
                        views: [[false, "form"]],
                        target: "current",
                    });
                },
            };
        });
    },

    async setCommands(namespace, options = {}) {
        await super.setCommands(namespace, options);

        const searchValue = (options.searchValue || "").trim();
        this.state.commands = this.state.commands.filter(
            (command) => command.category !== "records"
        );

        if (!searchValue || searchValue.length < 2) {
            this.categoryKeys = this.categoryKeys.filter(
                (key) => key !== "records"
            );
            delete this.categoryNames.records;
            this.recordSearchSequence++;
            if (this.recordSearchTimer) {
                clearTimeout(this.recordSearchTimer);
                this.recordSearchTimer = null;
            }
            return;
        }

        const recordCommands = await this.searchRecords(searchValue);

        if (!recordCommands.length) {
            this.categoryKeys = this.categoryKeys.filter(
                (key) => key !== "records"
            );
            delete this.categoryNames.records;
            return;
        }

        this.state.commands = [
            ...this.state.commands,
            ...recordCommands,
        ];

        if (!this.categoryKeys.includes("records")) {
            this.categoryKeys = [
                ...this.categoryKeys,
                "records",
            ];
        }

        this.categoryNames = {
            ...this.categoryNames,
            records: _t("Records"),
        };
    },

});

