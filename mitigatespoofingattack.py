import switchconfiguration
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import time
class ThroughputMonitor(switchconfiguration.SimpleSwitch13):
   # OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ThroughputMonitor, self).__init__(*args, **kwargs)
        #collects the throughput in every switch
        self.flow_file = open('flow_throughput.csv', 'w')
        self.flow_file.write('Switch,Flow Rules,Throughput(bps)\n')
        self.flow_file.close()
        self.datapaths = {}
        #self.monitor_time = time.time()
        self.flowswitch=[[1,0,0],[2,0,0],[3,0,0]]
        self.monitor_request()
    #Asynchronous message
    @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath

        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]


    #@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    #def packet_in_handler(self, ev):
        # ignore packet in messages
     #   pass

    #@set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    #def port_stats_reply_handler(self, ev):
        # ignore port stats messages
        #pass
    def monitor_request(self):
        while True:
            for dp in self.datapaths.values():
                self.request_stats(dp)
            self.flow_file = open('flow_throughput.csv','a+')
            self.flow_file.write("{} \n".format(self.flowswitch))
            self.flow_file.close()
            self.flowswitch=[[1,0,0],[2,0,0],[3,0,0]]
            self.monitor_time = time.time()

            time.sleep(60)

    def request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        self.switch_id = ev.msg.datapath.id
        if time.time() >= self.monitor_time+60:
            self.flowswitch[self.switch_id-1][1] +=len(ev.msg.body)
        for flow in ev.msg.body:
            self.flowswitch[self.switch_id-1][2] +=flow.byte_count
            #if flow.match == "OFPMatch(oxm_fields={})":
            #print(flow)
            #excludig the flow rules with priority =0 beacuse itd flwrule towards controller.
            if flow.priority != 0:
                #print(flow.table_id)
                # print(type(flow.duration_sec))
                actions=[]
                instruction=[]
                ofproto = ev.msg.datapath.ofproto
                parser = ev.msg.datapath.ofproto_parser
                actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL,0)]
                instruction=[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                priority = flow.priority
                if ((flow.duration_sec > 5) and (len(ev.msg.body)>1000)):
                    if flow.packet_count < 1:
                        instruction=[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                        command=ofproto.OFPFC_DELETE_STRICT
                        self.logger.info("flow rule deleted")
                    if flow.packet_count > 5:
                        priority = flow.packet.count
                        if flow.packet_count >50000:
                            priority = 51000
                        command = ofproto.OFPFC_MODIFY_STRICT
                        self.logger.info("flow rule modified")
                    mod = parser.OFPFlowMod(datapath = ev.msg.datapath, cookie=flow.cookie, cookie_mask = 0, table_id = flow.table_id, command=command,
                            idle_timeout = flow.idle_timeout, hard_timeout=flow.hard_timeout, priority = priority, buffer_id=ofproto.OFP_NO_BUFFER, out_port=ofproto.OFPP_ANY,out_group=ofproto.OFPG_ANY,
                            flags=ofproto.OFPFF_SEND_FLOW_REM,match=flow.match,instructions=instruction)
                    ev.msg.datapath.send_msg(mod)
                            





