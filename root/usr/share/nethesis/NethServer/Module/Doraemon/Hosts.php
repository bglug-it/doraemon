<?php

namespace NethServer\Module\Doraemon;


class Hosts extends \Nethgui\Controller\TableController
{

    public function initialize()
    {
        $columns = array(
            'Key',
            'MacAddress',
            'Role',
            'Actions',
        );

        $this
            ->setTableAdapter($this->getPlatform()->getTableAdapter('hosts', 'remote'))
            ->setColumns($columns)
       // TODO:
       //     ->addRowAction(new \NethServer\Module\Doraemon\Hosts\Modify('wake'))
       //     ->addRowAction(new \NethServer\Module\Doraemon\Hosts\Modify('reboot'))
       //     ->addRowAction(new \NethServer\Module\Doraemon\Hosts\Modify('shutdown'))
            ->addRowAction(new \NethServer\Module\Doraemon\Hosts\Modify('update'))
            ->addRowAction(new \NethServer\Module\Doraemon\Hosts\Modify('delete'))
            ->addTableAction(new \NethServer\Module\Doraemon\Hosts\Modify('create'))
            ->addTableAction(new \Nethgui\Controller\Table\Help('Help'))
        ;

        parent::initialize();
    }

}
