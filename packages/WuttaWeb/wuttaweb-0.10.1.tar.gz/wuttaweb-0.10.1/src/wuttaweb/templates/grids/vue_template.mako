## -*- coding: utf-8; -*-

<script type="text/x-template" id="${grid.vue_tagname}-template">
  <${b}-table :data="data"
              :loading="loading"
              narrowed
              hoverable
              icon-pack="fas"

              ## sorting
              % if grid.sortable:
                  ## nb. buefy/oruga only support *one* default sorter
                  :default-sort="sorters.length ? [sorters[0].field, sorters[0].order] : null"
                  % if grid.sort_on_backend:
                      backend-sorting
                      @sort="onSort"
                  % endif
                  % if grid.sort_multiple:
                      % if grid.sort_on_backend:
                          ## TODO: there is a bug (?) which prevents the arrow
                          ## from displaying for simple default single-column sort,
                          ## when multi-column sort is allowed for the table.  for
                          ## now we work around that by waiting until mount to
                          ## enable the multi-column support.  see also
                          ## https://github.com/buefy/buefy/issues/2584
                          :sort-multiple="allowMultiSort"
                          :sort-multiple-data="sortingPriority"
                          @sorting-priority-removed="sortingPriorityRemoved"
                      % else:
                          sort-multiple
                      % endif
                      ## nb. user must ctrl-click column header for multi-sort
                      sort-multiple-key="ctrlKey"
                  % endif
              % endif

              ## paging
              % if grid.paginated:
                  paginated
                  pagination-size="is-small"
                  :per-page="perPage"
                  :current-page="currentPage"
                  @page-change="onPageChange"
                  % if grid.paginate_on_backend:
                      backend-pagination
                      :total="pagerStats.item_count"
                  % endif
              % endif
              >

    % for column in grid.get_vue_columns():
        <${b}-table-column field="${column['field']}"
                           label="${column['label']}"
                           v-slot="props"
                          :sortable="${json.dumps(column.get('sortable', False))|n}"
                           cell-class="c_${column['field']}">
          % if grid.is_linked(column['field']):
              <a :href="props.row._action_url_view"
                 v-html="props.row.${column['field']}" />
          % else:
              <span v-html="props.row.${column['field']}"></span>
          % endif
        </${b}-table-column>
    % endfor

    % if grid.actions:
        <${b}-table-column field="actions"
                           label="Actions"
                           v-slot="props">
          % for action in grid.actions:
              <a v-if="props.row._action_url_${action.key}"
                 :href="props.row._action_url_${action.key}"
                 class="${action.link_class}">
                ${action.render_icon_and_label()}
              </a>
              &nbsp;
          % endfor
        </${b}-table-column>
    % endif

    <template #empty>
      <section class="section">
        <div class="content has-text-grey has-text-centered">
          <p>
            <b-icon
               pack="fas"
               icon="sad-tear"
               size="is-large">
            </b-icon>
          </p>
          <p>Nothing here.</p>
        </div>
      </section>
    </template>

    % if grid.paginated:
        <template #footer>
          <div style="display: flex; justify-content: space-between;">
            <div></div>
            <div v-if="pagerStats.first_item"
                 style="display: flex; gap: 0.5rem; align-items: center;">
              <span>
                showing
                {{ renderNumber(pagerStats.first_item) }}
                - {{ renderNumber(pagerStats.last_item) }}
                of {{ renderNumber(pagerStats.item_count) }} results;
              </span>
              <b-select v-model="perPage"
                        % if grid.paginate_on_backend:
                            @input="onPageSizeChange"
                        % endif
                        size="is-small">
                <option v-for="size in pageSizeOptions"
                        :value="size">
                  {{ size }}
                </option>
              </b-select>
              <span>
                per page
              </span>
            </div>
          </div>
        </template>
      % endif

  </${b}-table>
</script>

<script>

  let ${grid.vue_component}CurrentData = ${json.dumps(grid.get_vue_data())|n}

  const ${grid.vue_component}Data = {
      data: ${grid.vue_component}CurrentData,
      loading: false,

      ## sorting
      % if grid.sortable:
          sorters: ${json.dumps(grid.get_vue_active_sorters())|n},
          % if grid.sort_multiple:
              % if grid.sort_on_backend:
                  ## TODO: there is a bug (?) which prevents the arrow
                  ## from displaying for simple default single-column sort,
                  ## when multi-column sort is allowed for the table.  for
                  ## now we work around that by waiting until mount to
                  ## enable the multi-column support.  see also
                  ## https://github.com/buefy/buefy/issues/2584
                  allowMultiSort: false,
                  ## nb. this should be empty when current sort is single-column
                  % if len(grid.active_sorters) > 1:
                      sortingPriority: ${json.dumps(grid.get_vue_active_sorters())|n},
                  % else:
                      sortingPriority: [],
                  % endif
              % endif
          % endif
      % endif

      ## paging
      % if grid.paginated:
          pageSizeOptions: ${json.dumps(grid.pagesize_options)|n},
          perPage: ${json.dumps(grid.pagesize)|n},
          currentPage: ${json.dumps(grid.page)|n},
          % if grid.paginate_on_backend:
              pagerStats: ${json.dumps(grid.get_vue_pager_stats())|n},
          % endif
      % endif
  }

  const ${grid.vue_component} = {
      template: '#${grid.vue_tagname}-template',
      computed: {

          % if not grid.paginate_on_backend:

              pagerStats() {
                  const data = this.data
                  let last = this.currentPage * this.perPage
                  let first = last - this.perPage + 1
                  if (last > data.length) {
                      last = data.length
                  }
                  return {
                      'item_count': data.length,
                      'items_per_page': this.perPage,
                      'page': this.currentPage,
                      'first_item': first,
                      'last_item': last,
                  }
              },

          % endif
      },

      % if grid.sortable and grid.sort_multiple and grid.sort_on_backend:

            ## TODO: there is a bug (?) which prevents the arrow
            ## from displaying for simple default single-column sort,
            ## when multi-column sort is allowed for the table.  for
            ## now we work around that by waiting until mount to
            ## enable the multi-column support.  see also
            ## https://github.com/buefy/buefy/issues/2584
            mounted() {
                this.allowMultiSort = true
            },

      % endif

      methods: {

          renderNumber(value) {
              if (value != undefined) {
                  return value.toLocaleString('en')
              }
          },

          getBasicParams() {
              const params = {
                  % if grid.paginated and grid.paginate_on_backend:
                      pagesize: this.perPage,
                      page: this.currentPage,
                  % endif
              }
              % if grid.sortable and grid.sort_on_backend:
                  for (let i = 1; i <= this.sorters.length; i++) {
                      params['sort'+i+'key'] = this.sorters[i-1].field
                      params['sort'+i+'dir'] = this.sorters[i-1].order
                  }
              % endif
              return params
          },

          async fetchData() {

              let params = new URLSearchParams(this.getBasicParams())
              if (!params.has('partial')) {
                  params.append('partial', true)
              }
              params = params.toString()

              this.loading = true
              this.$http.get(`${request.path_url}?${'$'}{params}`).then(response => {
                  if (!response.data.error) {
                      ${grid.vue_component}CurrentData = response.data.data
                      this.data = ${grid.vue_component}CurrentData
                      % if grid.paginated and grid.paginate_on_backend:
                          this.pagerStats = response.data.pager_stats
                      % endif
                      this.loading = false
                  } else {
                      this.$buefy.toast.open({
                          message: data.error,
                          type: 'is-danger',
                          duration: 2000, // 4 seconds
                      })
                      this.loading = false
                  }
              })
              .catch((error) => {
                  this.data = []
                  % if grid.paginated and grid.paginate_on_backend:
                      this.pagerStats = {}
                  % endif
                  this.loading = false
                  throw error
              })
          },

          % if grid.sortable and grid.sort_on_backend:

              onSort(field, order, event) {

                  ## nb. buefy passes field name; oruga passes field object
                  % if request.use_oruga:
                      field = field.field
                  % endif

                  % if grid.sort_multiple:

                      // did user ctrl-click the column header?
                      if (event.ctrlKey) {

                          // toggle direction for existing, or add new sorter
                          const sorter = this.sorters.filter(s => s.field === field)[0]
                          if (sorter) {
                              sorter.order = sorter.order === 'desc' ? 'asc' : 'desc'
                          } else {
                              this.sorters.push({field, order})
                          }

                          // apply multi-column sorting
                          this.sortingPriority = this.sorters

                      } else {

                  % endif

                  // sort by single column only
                  this.sorters = [{field, order}]

                  % if grid.sort_multiple:
                          // multi-column sort not engaged
                          this.sortingPriority = []
                      }
                  % endif

                  // nb. always reset to first page when sorting changes
                  this.currentPage = 1
                  this.fetchData()
              },

              % if grid.sort_multiple:

                  sortingPriorityRemoved(field) {

                      // prune from active sorters
                      this.sorters = this.sorters.filter(s => s.field !== field)

                      // nb. even though we might have just one sorter
                      // now, we are still technically in multi-sort mode
                      this.sortingPriority = this.sorters

                      this.fetchData()
                  },

              % endif

          % endif

          % if grid.paginated:

              % if grid.paginate_on_backend:
                  onPageSizeChange(size) {
                      this.fetchData()
                  },
              % endif

              onPageChange(page) {
                  this.currentPage = page
                  % if grid.paginate_on_backend:
                      this.fetchData()
                  % endif
              },

          % endif
      },
  }

</script>
